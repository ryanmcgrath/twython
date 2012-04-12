#!/usr/bin/env python

"""
    Twython is a library for Python that wraps the Twitter API.
    It aims to abstract away all the API endpoints, so that additions to the library
    and/or the Twitter API won't cause any overall problems.

    Questions, comments? ryan@venodesigns.net
"""

__author__ = "Ryan McGrath <ryan@venodesigns.net>"
__version__ = "1.7.0"

import urllib
import re
import time

import requests
from oauth_hook import OAuthHook
import oauth2 as oauth

try:
    from urlparse import parse_qsl
except ImportError:
    from cgi import parse_qsl

# Twython maps keyword based arguments to Twitter API endpoints. The endpoints
# table is a file with a dictionary of every API endpoint that Twython supports.
from twitter_endpoints import base_url, api_table, twitter_http_status_codes


# There are some special setups (like, oh, a Django application) where
# simplejson exists behind the scenes anyway. Past Python 2.6, this should
# never really cause any problems to begin with.
try:
    # If they have the library, chances are they're gonna want to use that.
    import simplejson
except ImportError:
    try:
        # Python 2.6 and up
        import json as simplejson
    except ImportError:
        try:
            # This case gets rarer by the day, but if we need to, we can pull it from Django provided it's there.
            from django.utils import simplejson
        except:
            # Seriously wtf is wrong with you if you get this Exception.
            raise Exception("Twython requires the simplejson library (or Python 2.6) to work. http://www.undefined.org/python/")


class TwythonError(AttributeError):
    """
        Generic error class, catch-all for most Twython issues.
        Special cases are handled by TwythonAPILimit and TwythonAuthError.

        Note: To use these, the syntax has changed as of Twython 1.3. To catch these,
        you need to explicitly import them into your code, e.g:

        from twython import TwythonError, TwythonAPILimit, TwythonAuthError
    """
    def __init__(self, msg, error_code=None, retry_after=None):
        self.msg = msg
        self.error_code = error_code

        if error_code is not None and error_code in twitter_http_status_codes:
            self.msg = '%s: %s -- %s' % \
                        (twitter_http_status_codes[error_code][0],
                         twitter_http_status_codes[error_code][1],
                         self.msg)

        if error_code == 400 or error_code == 420:
            raise TwythonRateLimitError(self.msg,
                                        error_code,
                                        retry_after=retry_after)

    def __str__(self):
        return repr(self.msg)


class TwythonAuthError(TwythonError):
    """ Raised when you try to access a protected resource and it fails due to
        some issue with your authentication.
    """
    def __init__(self, msg, error_code=None):
        self.msg = msg
        self.error_code = error_code

    def __str__(self):
        return repr(self.msg)


class TwythonRateLimitError(TwythonError):
    """ Raised when you've hit a rate limit.
        retry_wait_seconds is the number of seconds to wait before trying again.
    """
    def __init__(self, msg, error_code, retry_after=None):
        retry_after = int(retry_after)
        self.msg = '%s (Retry after %s seconds)' % (msg, retry_after)
        TwythonError.__init__(self, msg, error_code)

    def __str__(self):
        return repr(self.msg)


''' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '''
''' REMOVE THE FOLLOWING IN TWYTHON 2.0 '''
''' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '''


class TwythonAPILimit(TwythonError):
    """ Raised when you've hit an API limit. Try to avoid these, read the API
        docs if you're running into issues here, Twython does not concern itself with
        this matter beyond telling you that you've done goofed.
    """
    def __init__(self, msg, error_code=None):
        self.msg = '%s\n Notice: APILimit is deprecated and soon to be removed, catch on TwythonRateLimitLimit instead!' % msg
        self.error_code = error_code

    def __str__(self):
        return repr(self.msg)


class APILimit(TwythonError):
    """ Raised when you've hit an API limit. Try to avoid these, read the API
        docs if you're running into issues here, Twython does not concern itself with
        this matter beyond telling you that you've done goofed.

        DEPRECATED, import and catch TwythonAPILimit instead.
    """
    def __init__(self, msg, error_code=None):
        self.msg = '%s\n Notice: APILimit is deprecated and soon to be removed, catch on TwythonRateLimitLimit instead!' % msg
        self.error_code = error_code

    def __str__(self):
        return repr(self.msg)


class AuthError(TwythonError):
    """ Raised when you try to access a protected resource and it fails due to some issue with
        your authentication.
    """
    def __init__(self, msg, error_code=None):
        self.msg = '%s\n Notice: AuthError is deprecated and soon to be removed, catch on TwythonAuthError instead!' % msg
        self.error_code = error_code

    def __str__(self):
        return repr(self.msg)

''' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '''
''' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '''


class Twython(object):
    def __init__(self, twitter_token=None, twitter_secret=None, oauth_token=None, oauth_token_secret=None, \
                headers=None, callback_url=None):
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

                ** Note: versioning is not currently used by search.twitter functions;
                         when Twitter moves their junk, it'll be supported.
        """
        OAuthHook.consumer_key = twitter_token
        OAuthHook.consumer_secret = twitter_secret

        # Needed for hitting that there API.
        self.request_token_url = 'http://twitter.com/oauth/request_token'
        self.access_token_url = 'http://twitter.com/oauth/access_token'
        self.authorize_url = 'http://twitter.com/oauth/authorize'
        self.authenticate_url = 'http://twitter.com/oauth/authenticate'
        self.api_url = 'http://api.twitter.com/%s/'

        self.twitter_token = twitter_token
        self.twitter_secret = twitter_secret
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_token_secret
        self.callback_url = callback_url

        # If there's headers, set them, otherwise be an embarassing parent for their own good.
        self.headers = headers
        if self.headers is None:
            self.headers = {'User-agent': 'Twython Python Twitter Library v' + __version__}

        self.client = None

        if self.twitter_token is not None and self.twitter_secret is not None:
            self.client = requests.session(hooks={'pre_request': OAuthHook()})

        if self.oauth_token is not None and self.oauth_secret is not None:
            self.oauth_hook = OAuthHook(self.oauth_token, self.oauth_secret, header_auth=True)
            self.client = requests.session(hooks={'pre_request': self.oauth_hook})

        # Filter down through the possibilities here - if they have a token, if they're first stage, etc.
        if self.client is None:
            # If they don't do authentication, but still want to request unprotected resources, we need an opener.
            self.client = requests.session()

        # register available funcs to allow listing name when debugging.
        def setFunc(key):
            return lambda **kwargs: self._constructFunc(key, **kwargs)
        for key in api_table.keys():
            self.__dict__[key] = setFunc(key)

        # create stash for last call intel
        self._last_call = None

    def _constructFunc(self, api_call, **kwargs):
        # Go through and replace any mustaches that are in our API url.
        fn = api_table[api_call]
        url = re.sub(
            '\{\{(?P<m>[a-zA-Z_]+)\}\}',
            # The '1' here catches the API version. Slightly hilarious.
            lambda m: "%s" % kwargs.get(m.group(1), '1'),
            base_url + fn['url']
        )

        method = fn['method'].lower()
        if not method in ('get', 'post', 'delete'):
            raise TwythonError('Method must be of GET, POST or DELETE')

        content = self._request(url, method=method, params=kwargs)

        return content

    def _request(self, url, method='GET', params=None, api_call=None):
        '''
        Internal response generator, not sense in repeating the same
        code twice, right? ;)
        '''
        myargs = {}
        method = method.lower()

        if method == 'get':
            url = '%s?%s' % (url, urllib.urlencode(params))
        else:
            myargs = params

        func = getattr(self.client, method)
        response = func(url, data=myargs)
        content = response.content.decode('utf-8')

        # create stash for last function intel
        self._last_call = {
            'api_call': api_call,
            'api_error': None,
            'cookies': response.cookies,
            'error': response.error,
            'headers': response.headers,
            'status_code': response.status_code,
            'url': response.url,
            'content': content,
        }

        # Python 2.6 `json` will throw a ValueError if it
        # can't load the string as valid JSON,
        # `simplejson` will throw simplejson.decoder.JSONDecodeError
        # But excepting just ValueError will work with both. o.O
        try:
            content = simplejson.loads(content)
        except ValueError:
            raise TwythonError('Response was not valid JSON, unable to decode.')

        if response.status_code > 304:
            # Just incase there is no error message, let's set a default
            error_msg = 'An error occurred processing your request.'
            if content.get('error') is not None:
                error_msg = content['error']

            self._last_call['api_error'] = error_msg

            raise TwythonError(error_msg,
                               error_code=response.status_code,
                               retry_after=response.headers.get('retry-after'))

        return content

    '''
    # Dynamic Request Methods
    Just in case Twitter releases something in their API
    and a developer wants to implement it on their app, but
    we haven't gotten around to putting it in Twython yet. :)
    '''

    def request(self, endpoint, method='GET', params=None, version=1):
        params = params or {}

        # In case they want to pass a full Twitter URL
        # i.e. http://search.twitter.com/
        if endpoint.startswith('http://'):
            url = endpoint
        else:
            url = '%s%s.json' % (self.api_url % version, endpoint)

        content = self._request(url, method=method, params=params, api_call=url)

        return content

    def get(self, endpoint, params=None, version=1):
        params = params or {}
        return self.request(endpoint, params=params, version=version)

    def post(self, endpoint, params=None, version=1):
        params = params or {}
        return self.request(endpoint, 'POST', params=params, version=version)

    def delete(self, endpoint, params=None, version=1):
        params = params or {}
        return self.request(endpoint, 'DELETE', params=params, version=version)

    # End Dynamic Request Methods

    def get_lastfunction_header(self, header):
        """
            get_lastfunction_header(self)

            returns the header in the last function
            this must be called after an API call, as it returns header based information.
            this will return None if the header is not present

            most useful for the following header information:
                x-ratelimit-limit
                x-ratelimit-remaining
                x-ratelimit-class
                x-ratelimit-reset
        """
        if self._last_call is None:
            raise TwythonError('This function must be called after an API call.  It delivers header information.')
        if header in self._last_call['headers']:
            return self._last_call['headers'][header]
        return None

    def get_authentication_tokens(self):
        """
            get_auth_url(self)

            Returns an authorization URL for a user to hit.
        """
        callback_url = self.callback_url

        request_args = {}
        if callback_url:
            request_args['oauth_callback'] = callback_url

        method = 'get'

        func = getattr(self.client, method)
        response = func(self.request_token_url, data=request_args)

        if response.status_code != 200:
            raise TwythonAuthError("Seems something couldn't be verified with your OAuth junk. Error: %s, Message: %s" % (response.status_code, response.content))

        request_tokens = dict(parse_qsl(response.content))
        if not request_tokens:
            raise TwythonError('Unable to decode request tokens.')

        oauth_callback_confirmed = request_tokens.get('oauth_callback_confirmed') == 'true'

        auth_url_params = {
            'oauth_token': request_tokens['oauth_token'],
        }

        # Use old-style callback argument if server didn't accept new-style
        if callback_url and not oauth_callback_confirmed:
            auth_url_params['oauth_callback'] = callback_url

        request_tokens['auth_url'] = self.authenticate_url + '?' + urllib.urlencode(auth_url_params)

        return request_tokens

    def get_authorized_tokens(self):
        """
            get_authorized_tokens

            Returns authorized tokens after they go through the auth_url phase.
        """
        response = self.client.get(self.access_token_url)
        authorized_tokens = dict(parse_qsl(response.content))
        if not authorized_tokens:
            raise TwythonError('Unable to decode authorized tokens.')

        return authorized_tokens

    # ------------------------------------------------------------------------------------------------------------------------
    # The following methods are all different in some manner or require special attention with regards to the Twitter API.
    # Because of this, we keep them separate from all the other endpoint definitions - ideally this should be change-able,
    # but it's not high on the priority list at the moment.
    # ------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def shortenURL(url_to_shorten, shortener="http://is.gd/api.php", query="longurl"):
        """
            shortenURL(url_to_shorten, shortener = "http://is.gd/api.php", query="longurl")

            Shortens url specified by url_to_shorten.
            Note: Twitter automatically shortens all URLs behind their own custom t.co shortener now,
                but we keep this here for anyone who was previously using it for alternative purposes. ;)

            Parameters:
                url_to_shorten - URL to shorten.
                shortener = In case you want to use a url shortening service other than is.gd.
        """
        request = requests.get('http://is.gd/api.php', params={
            'query': url_to_shorten
        })

        if request.status_code in [301, 201, 200]:
            return request.text
        else:
            raise TwythonError('shortenURL() failed with a %s error code.' % request.status_code , request.status_code )

    @staticmethod
    def constructApiURL(base_url, params):
        return base_url + "?" + "&".join(["%s=%s" % (Twython.unicode2utf8(key), urllib.quote_plus(Twython.unicode2utf8(value))) for (key, value) in params.iteritems()])

    def bulkUserLookup(self, ids=None, screen_names=None, version=1, **kwargs):
        """ A method to do bulk user lookups against the Twitter API.

            Documentation: https://dev.twitter.com/docs/api/1/get/users/lookup

            :ids or screen_names: (required)
            :param ids: (optional) A list of integers of Twitter User IDs
            :param screen_names: (optional) A list of strings of Twitter Screen Names

            :param include_entities: (optional) When set to either true, t or 1,
                                     each tweet will include a node called
                                     "entities,". This node offers a variety of
                                     metadata about the tweet in a discreet structure

            e.g x.bulkUserLookup(screen_names=['ryanmcgrath', 'mikehelmick'],
                                 include_entities=1)
        """
        if ids is None and screen_names is None:
            raise TwythonError('Please supply either a list of ids or \
                                screen_names for this method.')

        if ids is not None:
            kwargs['user_id'] = ','.join(map(str, ids))
        if screen_names is not None:
            kwargs['screen_name'] = ','.join(screen_names)

        return self.get('users/lookup', params=kwargs, version=version)

    def search(self, **kwargs):
        """ Returns tweets that match a specified query.

            Documentation: https://dev.twitter.com/

            :param q: (required) The query you want to search Twitter for

            :param geocode: (optional) Returns tweets by users located within
                            a given radius of the given latitude/longitude.
                            The parameter value is specified by
                            "latitude,longitude,radius", where radius units
                            must be specified as either "mi" (miles) or
                            "km" (kilometers).
                            Example Values: 37.781157,-122.398720,1mi
            :param lang: (optional) Restricts tweets to the given language,
                         given by an ISO 639-1 code.
            :param locale: (optional) Specify the language of the query you
                           are sending. Only ``ja`` is currently effective.
            :param page: (optional) The page number (starting at 1) to return
                         Max ~1500 results
            :param result_type: (optional) Default ``mixed``
                                mixed: Include both popular and real time
                                       results in the response.
                                recent: return only the most recent results in
                                        the response
                                popular: return only the most popular results
                                         in the response.

            e.g x.search(q='jjndf', page='2')
        """
        return self.get('http://search.twitter.com/search.json', params=kwargs)

    def searchGen(self, search_query, **kwargs):
        """ Returns a generator of tweets that match a specified query.

            Documentation: https://dev.twitter.com/doc/get/search.

            See Twython.search() for acceptable parameters

            e.g search = x.searchGen('python')
                for result in search:
                    print result
        """
        kwargs['q'] = search_query
        content = self.get('http://search.twitter.com/search.json', params=kwargs)

        if not content['results']:
            raise StopIteration

        for tweet in content['results']:
            yield tweet

        if 'page' not in kwargs:
            kwargs['page'] = '2'
        else:
            try:
                kwargs['page'] = int(kwargs['page'])
                kwargs['page'] += 1
                kwargs['page'] = str(kwargs['page'])
            except TypeError:
                raise TwythonError("searchGen() exited because page takes type str")

        for tweet in self.searchGen(search_query, **kwargs):
            yield tweet

    def isListMember(self, list_id, id, username, version=1, **kwargs):
        """ Check if a specified user (username) is a member of the list in question (list_id).

            Documentation: https://dev.twitter.com/docs/api/1/get/lists/members/show

            **Note: This method may not work for private/protected lists,
                    unless you're authenticated and have access to those lists.

            :param list_id: (required) The numerical id of the list.
            :param username: (required) The screen name for whom to return results for
            :param version: (optional) Currently, default (only effective value) is 1
            :param id: (deprecated) This value is no longer needed.

            e.g.
            **Note: currently TwythonError is not descriptive enough
                    to handle specific errors, those errors will be
                    included in the library soon enough
            try:
                x.isListMember(53131724, None, 'ryanmcgrath')
            except TwythonError:
                print 'User is not a member'
        """
        kwargs['list_id'] = list_id
        kwargs['screen_name'] = username
        return self.get('lists/members/show', params=kwargs)

    def isListSubscriber(self, username, list_id, id, version=1, **kwargs):
        """ Check if a specified user (username) is a subscriber of the list in question (list_id).

            Documentation: https://dev.twitter.com/docs/api/1/get/lists/subscribers/show

            **Note: This method may not work for private/protected lists,
                    unless you're authenticated and have access to those lists.

            :param list_id: (required) The numerical id of the list.
            :param username: (required) The screen name for whom to return results for
            :param version: (optional) Currently, default (only effective value) is 1
            :param id: (deprecated) This value is no longer needed.

            e.g.
            **Note: currently TwythonError is not descriptive enough
                    to handle specific errors, those errors will be
                    included in the library soon enough
            try:
                x.isListSubscriber('ryanmcgrath', 53131724, None)
            except TwythonError:
                print 'User is not a member'

            The above throws a TwythonError, the following returns data about
            the user since they follow the specific list:

            x.isListSubscriber('icelsius', 53131724, None)
        """
        kwargs['list_id'] = list_id
        kwargs['screen_name'] = username
        return self.get('lists/subscribers/show', params=kwargs)

    # The following methods are apart from the other Account methods,
    # because they rely on a whole multipart-data posting function set.
    def updateProfileBackgroundImage(self, file_, tile=True, version=1):
        """ updateProfileBackgroundImage(filename, tile=True)

            Updates the authenticating user's profile background image.

            Parameters:
                image - Required. Must be a valid GIF, JPG, or PNG image of less than 800 kilobytes in size. Images with width larger than 2048 pixels will be forceably scaled down.
                tile - Optional (defaults to True). If set to true the background image will be displayed tiled. The image will not be tiled otherwise.
                version (number) - Optional. API version to request. Entire Twython class defaults to 1, but you can override on a function-by-function or class basis - (version=2), etc.
        """
        url = 'http://api.twitter.com/%d/account/update_profile_background_image.json' % version
        return self._media_update(url,
                                  {'image': (file_, open(file_, 'rb'))},
                                  params={'tile': tile})

    def updateProfileImage(self, file_, version=1):
        """ updateProfileImage(filename)

            Updates the authenticating user's profile image (avatar).

            Parameters:
                image - Required. Must be a valid GIF, JPG, or PNG image of less than 700 kilobytes in size. Images with width larger than 500 pixels will be scaled down.
                version (number) - Optional. API version to request. Entire Twython class defaults to 1, but you can override on a function-by-function or class basis - (version=2), etc.
        """
        url = 'http://api.twitter.com/%d/account/update_profile_image.json' % version
        return self._media_update(url,
                                  {'image': (file_, open(file_, 'rb'))})

    # statuses/update_with_media
    def updateStatusWithMedia(self, file_, version=1, **params):
        """ updateStatusWithMedia(filename)

            Updates the authenticating user's profile image (avatar).

            Parameters:
                image - Required. Must be a valid GIF, JPG, or PNG image of less than 700 kilobytes in size. Images with width larger than 500 pixels will be scaled down.
                version (number) - Optional. API version to request. Entire Twython class defaults to 1, but you can override on a function-by-function or class basis - (version=2), etc.
        """
        url = 'https://upload.twitter.com/%d/statuses/update_with_media.json' % version
        return self._media_update(url,
                                  {'media': (file_, open(file_, 'rb'))},
                                  **params)

    def _media_update(self, url, file_, params=None):
        params = params or {}

        '''
        ***
        Techincally, this code will work one day. :P
        I think @kennethreitz is working with somebody to
        get actual OAuth stuff implemented into `requests`
        Until then we will have to use `request-oauth` and
        currently the code below should work, but doesn't.

        See this gist (https://gist.github.com/2002119)
        request-oauth is missing oauth_body_hash from the
        header.. that MIGHT be why it's not working..
        I haven't debugged enough.

                - Mike Helmick
        ***

        self.oauth_hook.header_auth = True
        self.client = requests.session(hooks={'pre_request': self.oauth_hook})
        print self.oauth_hook
        response = self.client.post(url, data=params, files=file_, headers=self.headers)
        print response.headers
        return response.content
        '''
        oauth_params = {
            'oauth_consumer_key': self.oauth_hook.consumer_key,
            'oauth_token': self.oauth_token,
            'oauth_timestamp': int(time.time()),
        }

        #create a fake request with your upload url and parameters
        faux_req = oauth.Request(method='POST', url=url, parameters=oauth_params)

        #sign the fake request.
        signature_method = oauth.SignatureMethod_HMAC_SHA1()

        class dotdict(dict):
            """
            This is a helper func. because python-oauth2 wants a
            dict in dot notation.
            """

            def __getattr__(self, attr):
                return self.get(attr, None)
            __setattr__ = dict.__setitem__
            __delattr__ = dict.__delitem__

        consumer = {
            'key': self.oauth_hook.consumer_key,
            'secret': self.oauth_hook.consumer_secret
        }
        token = {
            'key': self.oauth_token,
            'secret': self.oauth_secret
        }

        faux_req.sign_request(signature_method, dotdict(consumer), dotdict(token))

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
        url = "http://api.twitter.com/%s/users/profile_image/%s.json" % \
              (version, username)

        if size:
            url = self.constructApiURL(url, {'size': size})

        #client.follow_redirects = False
        response = self.client.get(url, allow_redirects=False)
        image_url = response.headers.get('location')

        if response.status_code in (301, 302, 303, 307) and image_url is not None:
            return image_url

        raise TwythonError("getProfileImageUrl() failed with a %d error code." % response.status_code, response.status_code)

    @staticmethod
    def stream(data, callback):
        """
            A Streaming API endpoint, because requests (by the lovely Kenneth Reitz) makes this not
            stupidly annoying to implement. In reality, Twython does absolutely *nothing special* here,
            but people new to programming expect this type of function to exist for this library, so we
            provide it for convenience.

            Seriously, this is nothing special. :)

            For the basic stream you're probably accessing, you'll want to pass the following as data dictionary
            keys. If you need to use OAuth (newer streams), passing secrets/etc as keys SHOULD work...

                username - Required. User name, self explanatory.
                password - Required. The Streaming API doesn't use OAuth, so we do this the old school way. It's all
                    done over SSL (https://), so you're not left totally vulnerable.
                endpoint - Optional. Override the endpoint you're using with the Twitter Streaming API. This is defaulted to the one
                    that everyone has access to, but if Twitter <3's you feel free to set this to your wildest desires.

            Parameters:
                data - Required. Dictionary of attributes to attach to the request (see: params https://dev.twitter.com/docs/streaming-api/methods)
                callback - Required. Callback function to be fired when tweets come in (this is an event-based-ish API).
        """
        endpoint = 'https://stream.twitter.com/1/statuses/filter.json'
        if 'endpoint' in data:
            endpoint = data.pop('endpoint')

        needs_basic_auth = False
        if 'username' in data:
            needs_basic_auth = True
            username = data.pop('username')
            password = data.pop('password')

        if needs_basic_auth:
            stream = requests.post(endpoint, data=data, auth=(username, password))
        else:
            stream = requests.post(endpoint, data=data)

        for line in stream.iter_lines():
            if line:
                callback(simplejson.loads(line))

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
        if isinstance(text, (str, unicode)):
            return Twython.unicode2utf8(text)
        return str(text)

    ''' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '''
    ''' REMOVE THE FOLLOWING IN TWYTHON 2.0 '''
    ''' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '''

    def searchTwitter(self, **kwargs):
        """use search() ,this is a fall back method to support searchTwitter()
        """
        return self.search(**kwargs)

    def searchTwitterGen(self, search_query, **kwargs):
        """use searchGen(), this is a fallback method to support
           searchTwitterGen()"""
        return self.searchGen(search_query, **kwargs)

    ''' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '''
