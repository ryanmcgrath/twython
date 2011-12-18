#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" 
    Twython is a library for Python that wraps the Twitter API.
    It aims to abstract away all the API endpoints, so that additions to the
    library and/or the Twitter API won't cause any overall problems.

    twythonrequests is twython implementation using requests.

    Questions, comments? ryan@venodesigns.net, me@kracekumar.com
"""

__author__ = "kracekumar <me@kracekumar.com>"
__version__ = "0.0.1"

""" 
    Importing requests and requests-oauth.
    requests supports 2.5 and above and no support for 3.x.

"""
from urlparse import parse_qs
from urllib2 import HTTPError
try:
    #Python 2.6 and up
    import requests
    import oauth_hook
except ImportError:
    raise Exception("twythonrequests requires requests - \
                     http://pypi.python.org/pypi/requests and \
                     requests-oauth -http://pypi.python.org/pypi/requests-oauth\
                     ")

#since requests support 2.5 and above, check for json and if fails check for\
#simplejson if that fails, requests installation must be broken.

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        # This must be dead code still worth 
        raise Exception("twythonrequests")

class TwythonError(AttributeError):
    """
        Generic error class, catch-all for most Twython issues.
        Special cases are handled by APILimit and AuthError.

        Note: To use these, the syntax has changed as of Twython 1.3. To catch \
        these, you need to explicitly import them into your code, e.g:

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
        docs if you're running into issues here, Twython does not concern \
        itself with this matter beyond telling you that you've done goofed.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class AuthError(TwythonError):
    """
        Raised when you try to access a protected resource and it fails due \
        to some issue with your authentication.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class Twython(object):
    def __init__(self, twitter_token = None, twitter_secret = None, \
                 oauth_token = None, oauth_token_secret = None, headers = None,\
                 callback_url = None):

        """ setup(self, oauth_token = None, headers = None)

            Instantiates an instance of Twython. 
            Takes optional parameters for authentication and such (see below).

            Parameters:
            twitter_token - Given to you when you register your application 
                            with Twitter.

            twitter_secret - Given to you when you register your application 
                             with Twitter.

            oauth_token - If you've gone through the authentication process 
                          and have a token for this user, pass it in and it'll 
                          be used for all requests going forward.
                                    
            oauth_token_secret - see oauth_token; it's the other half.

            headers - User agent header, dictionary style aka 
                                {'User-Agent': 'Bert'}
        """
        # API for accessing twitter data 
        self.request_token_url = "http://twitter.com/oauth/request_token"
        self.access_token_url = "http://twitter.com/oauth/access_token"
        self.authorize_url = "http://twitter.com/oauth/authorize"
        self.authenticate_url = "http://twitter.com/oauth/authenticate"
        self.twitter_token = twitter_token
        self.twitter_secret = twitter_secret
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_token_secret
        self.callback_url = callback_url or 'oob'
        self.oauth_hook = None
        self.client = None

        #In case headers are present lets add
        if headers is None:
            self.headers = {'User-agent': 'Twython python library v1.3 via \
                                           python-requests'}
        else:
            self.headers = headers

        #next is oauth, here we use requests-oauth
        if self.twitter_token:
            OAuthHook.consumer_key = self.twitter_token

        if self.twitter_secret:
            OAuthHook.consumer_secret = self.twitter_secret

        #if users pass oauth token and secret we initialize with oauth_hook
        #code taken from maraujop/requests-oauth
        if self.oauth_token and self.oauth_secret:
            #Creating OAuthHooks
            self.oauth_hook = oauth_hook.OAuthHook(self.oauth_auth_token,\
                                        self.ouath_secret)

            #real magic of requests start here
            self.client = requests.session(hooks={ 'pre_request': \
                                                    self.oauth_hook })
        else:
            if self.twitter_token and self.twitter_secret:
                self.oauth_hook = oauth_hook.OAuthhook(\
                                  consumer_key=self.twitter_token,\
                                  consumer_secret=self.twitter_secret)
                self.client = requests.session(hooks={'pre_request':\
                                                       self.oauth_hook})

    def __getattr__(self, api_call):
        pass

    def get(self, **kwargs):
        pass

    def get_authorized_tokens(self):
        return self.get_authentication_tokens(internal = 1)

    def get_authentication_tokens(self, internal = None):
        """
            get_auth_url(self)

            Returns an authorization URL for a user to hit.
        """
        if internal:
            self.response = self.client.post(self.request_token_url,\
                                        {'oauth_callback': self.callback_url})
        else:
            self.response = self.client.get(self.request_token_url)

        if self.response.code == 200:
            self.response = parse_qs(self.response.content)
            try:
                return {'oauth_token': self.response['oauth_token'],\
                        'oauth_secret': self.response['oauth_token_secret']}
            except AttributeError, e:
                raise TwythonError("Something went wrong, with parsing or call\
                \n get_authentication_token() failed with %s error code"% \
                `e.code`)
        else:
            raise AuthError("Something went wrong\nError code:%s\n\
                             Error Message:%s"%(self.response.status_code,\
                                                self.response.error.msg))  


    @staticmethod
    def shortenURL(url_to_shorten):
        """ 
            This is the function which will shorten url.
            It uses is.gd.
            Url: http://is.gd/create.php

            Parameters:
              url_to_shorten - string - Long url which is to be shortened.
              
            Returns shorten url which is in unicode format.
        """
        try:
            response = requests.post("http://is.gd/create.php", \
                            data={'format': 'simple', 'url': url_to_shorten})
            response.raise_for_status()
            return response.content
        except HTTPError, e:
            raise TwythonError("shortenURL() failed with a %s error code."\
                                                          % `e.code`, e.code)
        

    def bulkUserLookup(self, ids = None, screen_names = None, version = 1,\
                                                              **kwargs):
        """
            bulkUserLookup(self, ids = None, screen_names = None, version = 1,
                                                                   **kwargs):

            A method to do bulk user lookups against the Twitter API.
            Arguments (ids (numbers) / screen_names (strings)) should be flat.
            Arrays that contain their respective data sets.

            Statuses for the users in question will be returned inline if they
            exists. Requires authentication!
        """
        if ids:
            kwargs['user_id'] = ','.join(map(str, ids))
        if screen_names:
            kwargs['screen_name'] = ','.join(screen_names)

        try:
            self.response = requests.get("\
                        http://api.twitter.com/%d/users/lookup.json" %version,\
                        kwargs)
            self.response.raise_for_status()
            return json.loads(self.response.content)
        except HTTPError, e:
            raise TwythonError("bulkUserLookup() failed with a %s error code."\
                                                          % `e.code`, e.code)

    def search(self, q, **kwargs):
        """
            search(**kwargs)
               

            Returns Tweets that match the specified query.

            Parameters:

               q: query to search for example

                   See the documentation at http://dev.twitter.com/doc/get/
                   search.

                   Pass in the API supported arguments as named parameters.

                   e.g: x.search(q='python', page='2')

        """
        try:
            self.response = requests.get(\
                                       "http://search.twitter.com/search.json",\
                                        params={'q': q}, **kwargs)
            self.response.raise_for_status()
            return json.loads(self.response.content)
        except HTTPError, e:
            raise TwythonError("search() failed with %s error code" \
                                   % `e.code`, e.code)

    def searchTwitter(self, q, **kwargs):
        """
           use search(). This will be removed soon.
        """
        return self.search(q, **kwargs)

    def searchGen(self, q, **kwargs):
        """
           seaarchGen(self, **kwargs)

           Returns a generator of tweets that match a specified query.

           Documentation: http://dev.twitter.com/doc/get/search

           e.g: x.searchGen(q='python', page='2')

         """
        try:
            self.response = self.search(q, **kwargs)
            self.response.raise_for_status()
            self.response = json.loads(self.response.content)
        except HTTPError, e:
            raise TwythonError("searchGen() exited with %d status code and \
                                    code "%self.response.status_code, e.code)

        if self.response['results']:
            raise StopIteration
        else:
            for tweet in data['results']:
                yield tweet

        if 'page' not in kwargs:
            kwargs['page'] = 2
        else:
            try:
            # This line converts page param in query parameter to int and 
            # adds one because we are running inside func which will yield
            # list of tweet using generator and converts to string.
                kwargs['page'] = str(int(kwargs['page']) + 1)
            except TypeError:
                raise TwythonError("searchGen() exited because it page \
                                        takes string ")
            except e:
                raise TwythonError("searchGen() failed with %s error code"%\
                                        `e.code`, e.code)

        for tweet in self.searchGen(**kwargs):
            yield tweet


    def searchTwitterGen(self, q, **kwargs):
        """
            use searchGen(). This will be removed soon.
         """
        return self.searchGen(q, **kwargs)
                    
    def isListMember(self, list_id, id, username, version = 1):
        """
            isListMember(self, list_id, id, username, version =1)

            Check if a specified user(id) is a member of the list in question
               (list_id)

           **Note: This method may not work for private/protected lists,
                 unless you're authenticated and have access to those lists.

            Parameters:
                    list_id - Required. The slug of the list to check against.
                    id - Required. The ID of the user being checked in the list.
                    username - User who owns the list you're checking against\
                    (username) version(number) - Optional. API version to \
                    request.\

                    version (number) - Optional. API version to request.

                    Entire Twython class defaults to 1, but you can override on\

                    a function-by-function or class basis - (version=2), etc.
        """
        try:
            self.response = requests.post("http://api.twitter.com/%d/%s/%s/\
                                members/%s.json" % (version, username, list_id,\
                                `id`), headers = self.headers)
            self.response.raise_for_status()
            return json.loads(Self.response.content)
        except HTTPError, e:
            raise TwythonError("isListMember() failed with status code %d"\
                      %self.response.status_code, e.code)

    def isListSubscriber(self, username, list_id, version = 1):
        """
            isListSubscriber(self, username, list_id, id, version)

            Check if a specified user(id) is a subscriber of the list in \
            question(list_id)

            **Note: This method may not work for private/protected lists,
                 unless you're authenticated and have access to those lists.

            Parameters:
                    list_id - Required. The slug of the list to check against.
                    id - Required. The ID of the user being checked in the list.
                    username - Required. The username of the owner of the list\
                    that you're seeing if someone is subscribed to.

                    version (number) - Optional. API version to request.
                    Entire Twython class defaults to 1, but you can override on\
                    a function-by-function or class basis - (version=2), etc.
        """
        try:
            self.response = requests.post("http://api.twitter.com/%d/%s/%s\
                                following/%s.json" % (version,username,list_id,\
                                `id`), headers = self.headers)
            self.response.raise_for_status()
            return json.loads(self.response.content)
        except HTTPError, e:
            raise TwythonError("isListMember() failed with %d error code."%\
                                    self.response.status_code, e.code)

    def updateProfileBackgroundImage(self,filename,tile="true",version=1):
        """
            updateProfileBackgroundImage(filename,tile="true")

            Updates the authenticating user's profile background image.

               Parameters:
                    image - Required. Must be a valid GIF, JPG, or PNG image of\
                    less than 800 kilobytes in size. Images with with larger \
                    than 2048 pixels will be forceably scaled down.

                    tile - Optional (defaults to true). If set to true the \
                           background image will be displayed tiled.
                           The image will not be tiled otherwise.

                    ** Note: It's sad, but when using this method, pass the \
                             tile value as string,

                             e.g. title="false"

                    version (number) - Optional. API version to request.\
                    Entire Twython class defaults to 1, but you can override on\
                    a function-by-function or class basis - (version=2), etc.
                       
        """
        url = "http://api.twitter.com/%d/account/update_profile_background.\
                   json?tile=%s" %(version,tile)
        try:
            files = {filename: open(filename, 'rb')}
        except IOError, e:
            raise TwythonError("file reading %d error"%`e.code`, e.code)

        try:
            self.response = request.post(url, files=files)
            self.response.raise_for_status()
            return self.response.status_code
        except HTTPError, e:
            raise Twython("updateProfileBackgroundImage failed with %d\
                               error code"%self.response.status_code, e.code)

    def updateProfileImage(self,filename,version=1):
        """
            updateProfileImage(filename)

            Updates the authenticating user's profile image (avatar).

            Parameters:
                    image - Required. Must be valid GIF, JPG, or PNG image of\
                    less than 700 kilobytes in size. Image with width larger \
                    than 500 pixels will be scaled down.

                    version (number) - Optional. API version to request.

                    Entire Twython class defaults to 1, but you can override on\
                    a function-by-function or class basis - (version=2), etc.

        """
        url = "http://api.twitter.com/%d/account/update_profile_image.json"\
                  %version
        try:
            files = {filename: open(filename, 'rb')}
        except IOError, e:
            raise TwythonError("file reading %d error"%`e.code`, e.code)

        try:
            self.response = requests.post(url, files=files)
            self.response.raise_for_status()
            return self.response.status_code
        except HTTPError, e:
            raise TwythonError("updateProfileImage() failed with %d error\
                      code"% self.response.status_code, e.code)

    def getProfileImageUrl(self, username, size=None, version=1):
        """
               getProfileImageUrl(username)

               Gets the URL for the user's profile image.

               Parameters:
                   username - Required. User name of the user you want the image
                   url of.

                   size - Optional.Options 'normal', 'mini', 'bigger'. Defaults
                   to 'normal' if not given.

                   version (number) - Optional. API version to request.

                   Entire Twython class defaults to 1, but you can override on\
                   a function-by-function or class basis - (version=2), etc.

        """
        url = "http://api.twitter.com/%s/users/profile_image/%s.json"%\
                   (version, username)
        try:
            self.response = requests.get(url, params={'size': size})
            if self.response.status_code in (301, 302, 303, 307):
                return self.response.headers['location']
            elif self.response.status_code == 200:
                return self.response.url
            self.response.raise_for_status()
        except HTTPError, e:
            raise TwythonError("getProfileIMageUrl() failed with %d \
                                       error code"% `e.code`, e.code)

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






                
                
