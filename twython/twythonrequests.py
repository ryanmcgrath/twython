#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" 
    Twython is a library for Python that wraps the Twitter API.
    It aims to abstract away all the API endpoints, so that additions to the
    library and/or the Twitter API won't cause any overall problems.

    twythonrequests is twython implementation using requests.

    Questions, comments? ryan@venodesigns.net, me@kracekumar.com
"""

__author__ = "kracekumar"
__version__ = "0.1"

""" 
    Importing requests and requests-oauth.
    requests supports 2.5 and above and no support for 3.x.

"""
import mimetypes
import mimetools
import re
import inspect
from urlparse import parse_qs

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

#imports required for Error Handling. Now I am importing from twython file in 
# future, it will be include in the same file, Hope ryan agrees :)
from twython import TwythonError, APILimit, RateLimitError, AuthError

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
                        'oauth_secret': self.response['oauth_token_secret'])}
            except AttributeError, e:
                raise TwythonError("Something went wrong, with parsing or call\
                \n get_authentication_token() failed with %s error code"% \
                `e.code`)
        else:
            raise AuthError("Something went wrong\nError code:%s\n\
                             Error Message:%s"%(self.response.status_code,\
                                                self.response.error.msg))  


                










