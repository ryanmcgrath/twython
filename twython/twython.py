#!/usr/bin/env python

"""
    Twython is a library for Python that wraps the Twitter API.
    It aims to abstract away all the API endpoints, so that additions to the library
    and/or the Twitter API won't cause any overall problems.

    Questions, comments? ryan@venodesigns.net
"""

__author__ = "Ryan McGrath <ryan@venodesigns.net>"
__version__ = "1.4.6"

import cgi
import urllib
import urllib2
import urlparse
import httplib
import httplib2
import mimetypes
import mimetools
import re
import inspect
import time

import requests
import oauth2 as oauth

try:
    from urlparse import parse_qsl
except ImportError:
    from cgi import parse_qsl

# Twython maps keyword based arguments to Twitter API endpoints. The endpoints
# table is a file with a dictionary of every API endpoint that Twython supports.
from twitter_endpoints import base_url, api_table

from urllib2 import HTTPError

# There are some special setups (like, oh, a Django application) where
# simplejson exists behind the scenes anyway. Past Python 2.6, this should
# never really cause any problems to begin with.
try:
    # Python 2.6 and up
    import json as simplejson
except ImportError:
    try:
        # Python 2.6 and below (2.4/2.5, 2.3 is not guranteed to work with this library to begin with)
        import simplejson
    except ImportError:
        try:
            # This case gets rarer by the day, but if we need to, we can pull it from Django provided it's there.
            from django.utils import simplejson
        except:
            # Seriously wtf is wrong with you if you get this Exception.
            raise Exception("Twython requires the simplejson library (or Python 2.6) to work. http://www.undefined.org/python/")

# Try and gauge the old OAuth2 library spec. Versions 1.5 and greater no longer have the callback
# url as part of the request object; older versions we need to patch for Python 2.5... ugh. ;P
OAUTH_CALLBACK_IN_URL = False
OAUTH_LIB_SUPPORTS_CALLBACK = False
if not hasattr(oauth, '_version') or float(oauth._version.manual_verstr) <= 1.4:
    OAUTH_CLIENT_INSPECTION = inspect.getargspec(oauth.Client.request)
    try:
        OAUTH_LIB_SUPPORTS_CALLBACK = 'callback_url' in OAUTH_CLIENT_INSPECTION.args    
    except AttributeError:
        # Python 2.5 doesn't return named tuples, so don't look for an args section specifically.
        OAUTH_LIB_SUPPORTS_CALLBACK = 'callback_url' in OAUTH_CLIENT_INSPECTION
else:
    OAUTH_CALLBACK_IN_URL = True

class TwythonError(AttributeError):
    """
        Generic error class, catch-all for most Twython issues.
        Special cases are handled by APILimit and AuthError.

        Note: To use these, the syntax has changed as of Twython 1.3. To catch these,
        you need to explicitly import them into your code, e.g:

        from twython import TwythonError, APILimit, AuthError
    """
    def __init__(self, msg, error_code=None):
        self.msg = msg
        if error_code == 400:
            raise APILimit(msg)

    def __str__(self):
        return repr(self.msg)


class APILimit(TwythonError):
    """
        Raised when you've hit an API limit. Try to avoid these, read the API
        docs if you're running into issues here, Twython does not concern itself with
        this matter beyond telling you that you've done goofed.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class RateLimitError(TwythonError):
    """
        Raised when you've hit a rate limit.  retry_wait_seconds is the number of seconds to
        wait before trying again.
    """
    def __init__(self, msg, retry_wait_seconds, error_code):
        self.retry_wait_seconds = int(retry_wait_seconds)
        TwythonError.__init__(self, msg, error_code)

    def __str__(self):
        return repr(self.msg)


class AuthError(TwythonError):
    """
        Raised when you try to access a protected resource and it fails due to some issue with
        your authentication.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class Twython(object):
    def __init__(self, twitter_token = None, twitter_secret = None, oauth_token = None, oauth_token_secret = None, headers=None, callback_url=None, client_args={}):
        """setup(self, oauth_token = None, headers = None)

            Instantiates an instance of Twython. Takes optional parameters for authentication and such (see below).

            Parameters:
                twitter_token - Given to you when you register your application with Twitter.
                twitter_secret - Given to you when you register your application with Twitter.
                oauth_token - If you've gone through the authentication process and have a token for this user,
                    pass it in and it'll be used for all requests going forward.
                oauth_token_secret - see oauth_token; it's the other half.
                headers - User agent header, dictionary style ala {'User-Agent': 'Bert'}
                client_args - additional arguments for HTTP client (see httplib2.Http.__init__), e.g. {'timeout': 10.0}

                ** Note: versioning is not currently used by search.twitter functions; when Twitter moves their junk, it'll be supported.
        """
        # Needed for hitting that there API.
        self.request_token_url = 'http://twitter.com/oauth/request_token'
        self.access_token_url = 'http://twitter.com/oauth/access_token'
        self.authorize_url = 'http://twitter.com/oauth/authorize'
        self.authenticate_url = 'http://twitter.com/oauth/authenticate'
        self.twitter_token = twitter_token
        self.twitter_secret = twitter_secret
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_token_secret
        self.callback_url = callback_url

        # If there's headers, set them, otherwise be an embarassing parent for their own good.
        self.headers = headers
        if self.headers is None:
            self.headers = {'User-agent': 'Twython Python Twitter Library v1.3'}

        self.consumer = None
        self.token = None

        if self.twitter_token is not None and self.twitter_secret is not None:
            self.consumer = oauth.Consumer(self.twitter_token, self.twitter_secret)

        if self.oauth_token is not None and self.oauth_secret is not None:
            self.token = oauth.Token(oauth_token, oauth_token_secret)

        # Filter down through the possibilities here - if they have a token, if they're first stage, etc.
        if self.consumer is not None and self.token is not None:
            self.client = oauth.Client(self.consumer, self.token, **client_args)
        elif self.consumer is not None:
            self.client = oauth.Client(self.consumer, **client_args)
        else:
            # If they don't do authentication, but still want to request unprotected resources, we need an opener.
            self.client = httplib2.Http(**client_args)
        # register available funcs to allow listing name when debugging.
        def setFunc(key):
            return lambda **kwargs: self._constructFunc(key, **kwargs)
        for key in api_table.keys():
            self.__dict__[key] = setFunc(key)

    def _constructFunc(self, api_call, **kwargs):
        # Go through and replace any mustaches that are in our API url.
        fn = api_table[api_call]
        base = re.sub(
            '\{\{(?P<m>[a-zA-Z_]+)\}\}',
            # The '1' here catches the API version. Slightly
            # hilarious.
            lambda m: "%s" % kwargs.get(m.group(1), '1'),
            base_url + fn['url']
        )

        # Then open and load that shiiit, yo. TODO: check HTTP method
        # and junk, handle errors/authentication
        if fn['method'] == 'POST':
            myargs = urllib.urlencode(dict([k, Twython.encode(v)] for k, v in kwargs.items()))
            resp, content = self.client.request(base, fn['method'], myargs, headers = self.headers)
        else:
            myargs = ["%s=%s" %(key, value) for (key, value) in kwargs.iteritems()]
            url = "%s?%s" %(base, "&".join(myargs))
            resp, content = self.client.request(url, fn['method'], headers=self.headers)

        return simplejson.loads(content.decode('utf-8'))

    def get_authentication_tokens(self):
        """
            get_auth_url(self)

            Returns an authorization URL for a user to hit.
        """
        callback_url = self.callback_url or 'oob'
        
        request_args = {}
        if OAUTH_LIB_SUPPORTS_CALLBACK:
            request_args['callback_url'] = callback_url
        
        resp, content = self.client.request(self.request_token_url, "GET", **request_args)

        if resp['status'] != '200':
            raise AuthError("Seems something couldn't be verified with your OAuth junk. Error: %s, Message: %s" % (resp['status'], content))
        
        request_tokens = dict(parse_qsl(content))
        
        oauth_callback_confirmed = request_tokens.get('oauth_callback_confirmed')=='true'
        
        if not OAUTH_LIB_SUPPORTS_CALLBACK and callback_url != 'oob' and oauth_callback_confirmed:
            import warnings
            warnings.warn("oauth2 library doesn't support OAuth 1.0a type callback, but remote requires it") 
            oauth_callback_confirmed = False

        auth_url_params = {
            'oauth_token' : request_tokens['oauth_token'],
        }
        
        # Use old-style callback argument
        if OAUTH_CALLBACK_IN_URL or (callback_url!='oob' and not oauth_callback_confirmed):
            auth_url_params['oauth_callback'] = callback_url
        
        request_tokens['auth_url'] = self.authenticate_url + '?' + urllib.urlencode(auth_url_params)
        
        return request_tokens

    def get_authorized_tokens(self):
        """
            get_authorized_tokens

            Returns authorized tokens after they go through the auth_url phase.
        """
        resp, content = self.client.request(self.access_token_url, "GET")
        return dict(parse_qsl(content))
    
    # ------------------------------------------------------------------------------------------------------------------------
    # The following methods are all different in some manner or require special attention with regards to the Twitter API.
    # Because of this, we keep them separate from all the other endpoint definitions - ideally this should be change-able,
    # but it's not high on the priority list at the moment.
    # ------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def constructApiURL(base_url, params):
        return base_url + "?" + "&".join(["%s=%s" %(Twython.unicode2utf8(key), urllib.quote_plus(Twython.unicode2utf8(value))) for (key, value) in params.iteritems()])

    @staticmethod
    def shortenURL(url_to_shorten, shortener = "http://is.gd/api.php", query = "longurl"):
        """shortenURL(url_to_shorten, shortener = "http://is.gd/api.php", query = "longurl")

            Shortens url specified by url_to_shorten.

            Parameters:
                url_to_shorten - URL to shorten.
                shortener - In case you want to use a url shortening service other than is.gd.
        """
        try:
            content = urllib2.urlopen(shortener + "?" + urllib.urlencode({query: Twython.unicode2utf8(url_to_shorten)})).read()
            return content
        except HTTPError, e:
            raise TwythonError("shortenURL() failed with a %s error code." % `e.code`)

    def bulkUserLookup(self, ids = None, screen_names = None, version = 1, **kwargs):
        """ bulkUserLookup(self, ids = None, screen_names = None, version = 1, **kwargs)

            A method to do bulk user lookups against the Twitter API. Arguments (ids (numbers) / screen_names (strings)) should be flat Arrays that
            contain their respective data sets.

            Statuses for the users in question will be returned inline if they exist. Requires authentication!
        """
        if ids:
            kwargs['user_id'] = ','.join(map(str, ids))
        if screen_names:
            kwargs['screen_name'] = ','.join(screen_names)
            
        lookupURL = Twython.constructApiURL("http://api.twitter.com/%d/users/lookup.json" % version, kwargs)
        try:
            resp, content = self.client.request(lookupURL, "POST", headers = self.headers)
            return simplejson.loads(content.decode('utf-8'))
        except HTTPError, e:
            raise TwythonError("bulkUserLookup() failed with a %s error code." % `e.code`, e.code)

    def search(self, **kwargs):
        """search(search_query, **kwargs)

            Returns tweets that match a specified query.

            Parameters:
                See the documentation at http://dev.twitter.com/doc/get/search. Pass in the API supported arguments as named parameters.

                e.g x.search(q = "jjndf", page = '2')
        """
        searchURL = Twython.constructApiURL("http://search.twitter.com/search.json", kwargs)
        try:
            resp, content = self.client.request(searchURL, "GET", headers = self.headers)

            if int(resp.status) == 420:
                retry_wait_seconds = resp['retry-after']
                raise RateLimitError("getSearchTimeline() is being rate limited.  Retry after %s seconds." %
                                     retry_wait_seconds,
                                     retry_wait_seconds,
                                     resp.status)

            return simplejson.loads(content.decode('utf-8'))
        except HTTPError, e:
            raise TwythonError("getSearchTimeline() failed with a %s error code." % `e.code`, e.code)

    def searchTwitter(self, **kwargs):
        """use search() ,this is a fall back method to support searchTwitter()
        """
        return self.search(**kwargs)

    def searchGen(self, search_query, **kwargs):
        """searchGen(search_query, **kwargs)

            Returns a generator of tweets that match a specified query.

            Parameters:
                See the documentation at http://dev.twitter.com/doc/get/search. Pass in the API supported arguments as named parameters.

                e.g x.searchGen("python", page="2") or
                    x.searchGen(search_query = "python", page = "2")
        """
        searchURL = Twython.constructApiURL("http://search.twitter.com/search.json?q=%s" % Twython.unicode2utf8(search_query), kwargs)
        try:
            resp, content = self.client.request(searchURL, "GET", headers = self.headers)
            data = simplejson.loads(content.decode('utf-8'))
        except HTTPError, e:
            raise TwythonError("searchGen() failed with a %s error code." % `e.code`, e.code)

        if not data['results']:
            raise StopIteration

        for tweet in data['results']:
            yield tweet

        if 'page' not in kwargs:
            kwargs['page'] = '2'
        else:
            try:
                kwargs['page'] = int(kwargs['page'])
                kwargs['page'] += 1
                kwargs['page'] = str(kwargs['page'])
            except TypeError:
                raise TwythonError("searchGen() exited because page takes str")
            except e: 
               raise TwythonError("searchGen() failed with %s error code" %\
                                    `e.code`, e.code)

        for tweet in self.searchGen(search_query, **kwargs):
            yield tweet

    def searchTwitterGen(self, search_query, **kwargs):
        """use searchGen(), this is a fallback method to support
           searchTwitterGen()"""
        return self.searchGen(search_query, **kwargs)

    def isListMember(self, list_id, id, username, version = 1):
        """ isListMember(self, list_id, id, version)

            Check if a specified user (id) is a member of the list in question (list_id).

            **Note: This method may not work for private/protected lists, unless you're authenticated and have access to those lists.

            Parameters:
                list_id - Required. The slug of the list to check against.
                id - Required. The ID of the user being checked in the list.
                username - User who owns the list you're checking against (username)
                version (number) - Optional. API version to request. Entire Twython class defaults to 1, but you can override on a function-by-function or class basis - (version=2), etc.
        """
        try:
            resp, content = self.client.request("http://api.twitter.com/%d/%s/%s/members/%s.json" % (version, username, list_id, `id`), headers = self.headers)
            return simplejson.loads(content.decode('utf-8'))
        except HTTPError, e:
            raise TwythonError("isListMember() failed with a %d error code." % e.code, e.code)

    def isListSubscriber(self, username, list_id, id, version = 1):
        """ isListSubscriber(self, list_id, id, version)

            Check if a specified user (id) is a subscriber of the list in question (list_id).

            **Note: This method may not work for private/protected lists, unless you're authenticated and have access to those lists.

            Parameters:
                list_id - Required. The slug of the list to check against.
                id - Required. The ID of the user being checked in the list.
                username - Required. The username of the owner of the list that you're seeing if someone is subscribed to.
                version (number) - Optional. API version to request. Entire Twython class defaults to 1, but you can override on a function-by-function or class basis - (version=2), etc.
        """
        try:
            resp, content = self.client.request("http://api.twitter.com/%d/%s/%s/following/%s.json" % (version, username, list_id, `id`), headers = self.headers)
            return simplejson.loads(content.decode('utf-8'))
        except HTTPError, e:
            raise TwythonError("isListMember() failed with a %d error code." % e.code, e.code)

    # The following methods are apart from the other Account methods, because they rely on a whole multipart-data posting function set.
    def updateProfileBackgroundImage(self, file_, tile=True, version=1):
        """ updateProfileBackgroundImage(filename, tile=True)

            Updates the authenticating user's profile background image.

            Parameters:
                image - Required. Must be a valid GIF, JPG, or PNG image of less than 800 kilobytes in size. Images with width larger than 2048 pixels will be forceably scaled down.
                tile - Optional (defaults to True). If set to true the background image will be displayed tiled. The image will not be tiled otherwise.
                version (number) - Optional. API version to request. Entire Twython class defaults to 1, but you can override on a function-by-function or class basis - (version=2), etc.
        """
        return self._media_update('http://api.twitter.com/%d/account/update_profile_background_image.json' % version, {'image':(file_, open(file_, 'rb'))}, params={'tile':tile})

    def updateProfileImage(self, file_, version=1):
        """ updateProfileImage(filename)

            Updates the authenticating user's profile image (avatar).

            Parameters:
                image - Required. Must be a valid GIF, JPG, or PNG image of less than 700 kilobytes in size. Images with width larger than 500 pixels will be scaled down.
                version (number) - Optional. API version to request. Entire Twython class defaults to 1, but you can override on a function-by-function or class basis - (version=2), etc.
        """
        return self._media_update('http://api.twitter.com/%d/account/update_profile_image.json' % version, {'image':(file_, open(file_, 'rb'))})

    # statuses/update_with_media
    def updateStatusWithMedia(self, file_, version=1, **params):
        """ updateStatusWithMedia(filename)

            Updates the authenticating user's profile image (avatar).

            Parameters:
                image - Required. Must be a valid GIF, JPG, or PNG image of less than 700 kilobytes in size. Images with width larger than 500 pixels will be scaled down.
                version (number) - Optional. API version to request. Entire Twython class defaults to 1, but you can override on a function-by-function or class basis - (version=2), etc.
        """
        return self._media_update('https://upload.twitter.com/%d/statuses/update_with_media.json' % version, {'media':(file_, open(file_, 'rb'))}, **params)

    def _media_update(self, url, file_, params={}):
        oauth_params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(length=41),
            'oauth_timestamp': int(time.time()),
        }

        #create a fake request with your upload url and parameters
        faux_req = oauth.Request(method='POST', url=url, parameters=oauth_params)
    
        #sign the fake request.
        signature_method = oauth.SignatureMethod_HMAC_SHA1()
        faux_req.sign_request(signature_method, self.consumer, self.token)
    
        #create a dict out of the fake request signed params
        self.headers.update(faux_req.to_header())

        req = requests.post(url, data=params, files=file_, headers=self.headers)
        return req.content

        
    def getProfileImageUrl(self, username, size=None, version=1):
        """ getProfileImageUrl(username)
        
            Gets the URL for the user's profile image.
            
            Parameters:
                username - Required. User name of the user you want the image url of.
                size - Optional. Image size. Valid options include 'normal', 'mini' and 'bigger'. Defaults to 'normal' if not given.
                version (number) - Optional. API version to request. Entire Twython class defaults to 1, but you can override on a function-by-function or class basis - (version=2), etc.
        """
        url = "http://api.twitter.com/%s/users/profile_image/%s.json" % (version, username)
        if size:
            url = self.constructApiURL(url, {'size':size})
        
        client = httplib2.Http()
        client.follow_redirects = False
        resp, content = client.request(url, 'GET')
        
        if resp.status in (301,302,303,307):
            return resp['location']
        elif resp.status == 200:
            return simplejson.loads(content.decode('utf-8'))
        
        raise TwythonError("getProfileImageUrl() failed with a %d error code." % resp.status, resp.status)
    
    @staticmethod
    def unicode2utf8(text):
        try:
            if isinstance(text, unicode):
                text = text.encode('utf-8')
        except:
            pass
        return text

    @staticmethod
    def encode(text):
        if isinstance(text, (str,unicode)):
            return Twython.unicode2utf8(text)
        return str(text)
