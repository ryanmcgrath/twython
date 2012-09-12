#!/usr/bin/env python

"""
    Twython is a library for Python that wraps the Twitter API.
    It aims to abstract away all the API endpoints, so that additions to the library
    and/or the Twitter API won't cause any overall problems.

    Questions, comments? ryan@venodesigns.net
"""

__author__ = "Ryan McGrath <ryan@venodesigns.net>"
__version__ = "2.4.0"

import urllib
import re
import warnings

import requests
from requests.auth import OAuth1

try:
    from urlparse import parse_qsl
except ImportError:
    from cgi import parse_qsl

# Twython maps keyword based arguments to Twitter API endpoints. The endpoints
# table is a file with a dictionary of every API endpoint that Twython supports.
from twitter_endpoints import base_url, api_table, twitter_http_status_codes

try:
    import simplejson
except ImportError:
    try:
        # Python 2.6 and up
        import json as simplejson
    except ImportError:
        try:
            from django.utils import simplejson
        except:
            # Seriously wtf is wrong with you if you get this Exception.
            raise Exception("Twython requires the simplejson library (or Python 2.6) to work. http://www.undefined.org/python/")


class TwythonError(Exception):
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

    def __str__(self):
        return repr(self.msg)


class TwythonAuthError(TwythonError):
    """ Raised when you try to access a protected resource and it fails due to
        some issue with your authentication.
    """
    pass


class TwythonRateLimitError(TwythonError):
    """ Raised when you've hit a rate limit.
        retry_wait_seconds is the number of seconds to wait before trying again.
    """
    def __init__(self, msg, error_code, retry_after=None):
        TwythonError.__init__(self, msg, error_code=error_code)
        if isinstance(retry_after, int):
            self.msg = '%s (Retry after %d seconds)' % (msg, retry_after)


class Twython(object):
    def __init__(self, app_key=None, app_secret=None, oauth_token=None, oauth_token_secret=None, \
                headers=None, callback_url=None, twitter_token=None, twitter_secret=None, proxies=None):
        """Instantiates an instance of Twython. Takes optional parameters for authentication and such (see below).

            :param app_key: (optional) Your applications key
            :param app_secret: (optional) Your applications secret key
            :param oauth_token: (optional) Used with oauth_token_secret to make authenticated calls
            :param oauth_token_secret: (optional) Used with oauth_token to make authenticated calls
            :param headers: (optional) Custom headers to send along with the request
            :param callback_url: (optional) If set, will overwrite the callback url set in your application
            :param proxies: (optional) A dictionary of proxies, for example {"http":"proxy.example.org:8080", "https":"proxy.example.org:8081"}.
        """

        # Needed for hitting that there API.
        self.api_url = 'https://api.twitter.com/%s'
        self.request_token_url = self.api_url % 'oauth/request_token'
        self.access_token_url = self.api_url % 'oauth/access_token'
        self.authorize_url = self.api_url % 'oauth/authorize'
        self.authenticate_url = self.api_url % 'oauth/authenticate'

        # Enforce unicode on keys and secrets
        self.app_key = app_key and unicode(app_key) or twitter_token and unicode(twitter_token)
        self.app_secret = app_key and unicode(app_secret) or twitter_secret and unicode(twitter_secret)

        self.oauth_token = oauth_token and u'%s' % oauth_token
        self.oauth_token_secret = oauth_token_secret and u'%s' % oauth_token_secret

        self.callback_url = callback_url

        # If there's headers, set them, otherwise be an embarassing parent for their own good.
        self.headers = headers or {'User-Agent': 'Twython v' + __version__}

        # Allow for unauthenticated requests
        self.client = requests.session(proxies=proxies)
        self.auth = None

        if self.app_key is not None and self.app_secret is not None and \
        self.oauth_token is None and self.oauth_token_secret is None:
            self.auth = OAuth1(self.app_key, self.app_secret,
                               signature_type='auth_header')

        if self.app_key is not None and self.app_secret is not None and \
        self.oauth_token is not None and self.oauth_token_secret is not None:
            self.auth = OAuth1(self.app_key, self.app_secret,
                               self.oauth_token, self.oauth_token_secret,
                               signature_type='auth_header')

        if self.auth is not None:
            self.client = requests.session(headers=self.headers, auth=self.auth, proxies=proxies)

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

        content = self._request(url, method=fn['method'], params=kwargs)

        return content

    def _request(self, url, method='GET', params=None, files=None, api_call=None):
        '''Internal response generator, no sense in repeating the same
        code twice, right? ;)
        '''
        method = method.lower()
        if not method in ('get', 'post'):
            raise TwythonError('Method must be of GET or POST')

        params = params or {}

        func = getattr(self.client, method)
        if method == 'get':
            response = func(url, params=params)
        else:
            response = func(url, data=params, files=files)
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


        #  wrap the json loads in a try, and defer an error
        #  why? twitter will return invalid json with an error code in the headers
        json_error = False
        try:
            content = simplejson.loads(content)
        except ValueError:
            json_error= True
            content= {}

        if response.status_code > 304:
            # If there is no error message, use a default.
            error_msg = content.get(
                'error', 'An error occurred processing your request.')
            self._last_call['api_error'] = error_msg

            if response.status_code == 420:
                exceptionType = TwythonRateLimitError
            else:
                exceptionType = TwythonError

            raise exceptionType(error_msg,
                                error_code=response.status_code,
                                retry_after=response.headers.get('retry-after'))

        # if we have a json error here , then it's not an official TwitterAPI error
        if json_error:
            raise TwythonError('Response was not valid JSON, unable to decode.')

        return content

    '''
    # Dynamic Request Methods
    Just in case Twitter releases something in their API
    and a developer wants to implement it on their app, but
    we haven't gotten around to putting it in Twython yet. :)
    '''

    def request(self, endpoint, method='GET', params=None, files=None, version=1):
        # In case they want to pass a full Twitter URL
        # i.e. https://search.twitter.com/
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            url = endpoint
        else:
            url = '%s/%s.json' % (self.api_url % version, endpoint)

        content = self._request(url, method=method, params=params, files=files, api_call=url)

        return content

    def get(self, endpoint, params=None, version=1):
        return self.request(endpoint, params=params, version=version)

    def post(self, endpoint, params=None, files=None, version=1):
        return self.request(endpoint, 'POST', params=params, files=files, version=version)

    # End Dynamic Request Methods

    def get_lastfunction_header(self, header):
        """Returns the header in the last function
            This must be called after an API call, as it returns header based
            information.

            This will return None if the header is not present

            Most useful for the following header information:
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
        """Returns an authorization URL for a user to hit.
        """
        request_args = {}
        if self.callback_url:
            request_args['oauth_callback'] = self.callback_url

        response = self.client.get(self.request_token_url, params=request_args)

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
        if self.callback_url and not oauth_callback_confirmed:
            auth_url_params['oauth_callback'] = self.callback_url

        request_tokens['auth_url'] = self.authenticate_url + '?' + urllib.urlencode(auth_url_params)

        return request_tokens

    def get_authorized_tokens(self):
        """Returns authorized tokens after they go through the auth_url phase.
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
    def shortenURL(url_to_shorten, shortener='http://is.gd/api.php'):
        """Shortens url specified by url_to_shorten.
            Note: Twitter automatically shortens all URLs behind their own custom t.co shortener now,
                but we keep this here for anyone who was previously using it for alternative purposes. ;)

            :param url_to_shorten: (required) The URL to shorten
            :param shortener: (optional) In case you want to use a different
                              URL shortening service
        """
        if shortener == '':
            raise TwythonError('Please provide a URL shortening service.')

        request = requests.get(shortener, params={
            'query': url_to_shorten
        })

        if request.status_code in [301, 201, 200]:
            return request.text
        else:
            raise TwythonError('shortenURL() failed with a %s error code.' % request.status_code)

    @staticmethod
    def constructApiURL(base_url, params):
        return base_url + "?" + "&".join(["%s=%s" % (Twython.unicode2utf8(key), urllib.quote_plus(Twython.unicode2utf8(value))) for (key, value) in params.iteritems()])

    def search(self, **kwargs):
        """ Returns tweets that match a specified query.

            Documentation: https://dev.twitter.com/doc/get/search

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

        return self.get('https://search.twitter.com/search.json', params=kwargs)

    def searchGen(self, search_query, **kwargs):
        """ Returns a generator of tweets that match a specified query.

            Documentation: https://dev.twitter.com/doc/get/search

            See Twython.search() for acceptable parameters

            e.g search = x.searchGen('python')
                for result in search:
                    print result
        """
        kwargs['q'] = search_query
        content = self.get('https://search.twitter.com/search.json', params=kwargs)

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

    # The following methods are apart from the other Account methods,
    # because they rely on a whole multipart-data posting function set.
    def updateProfileBackgroundImage(self, file_, tile=True, version=1):
        """Updates the authenticating user's profile background image.

            :param file_: (required) A string to the location of the file
                          (less than 800KB in size, larger than 2048px width will scale down)
            :param tile: (optional) Default ``True`` If set to true the background image
                         will be displayed tiled. The image will not be tiled otherwise.
            :param version: (optional) A number, default 1 because that's the
                            only API version Twitter has now
        """
        url = 'https://api.twitter.com/%d/account/update_profile_background_image.json' % version
        return self._media_update(url,
                                  {'image': (file_, open(file_, 'rb'))},
                                  **{'tile': tile})

    def bulkUserLookup(self, **kwargs):
        """Stub for a method that has been deprecated, kept for now to raise errors
            properly if people are relying on this (which they are...).
        """
        warnings.warn(
            "This function has been deprecated. Please migrate to .lookupUser() - params should be the same.",
            DeprecationWarning,
            stacklevel=2
        )

    def updateProfileImage(self, file_, version=1):
        """Updates the authenticating user's profile image (avatar).

            :param file_: (required) A string to the location of the file
            :param version: (optional) A number, default 1 because that's the
                            only API version Twitter has now
        """
        url = 'https://api.twitter.com/%d/account/update_profile_image.json' % version
        return self._media_update(url,
                                  {'image': (file_, open(file_, 'rb'))})

    def updateStatusWithMedia(self, file_, version=1, **params):
        """Updates the users status with media

            :param file_: (required) A string to the location of the file
            :param version: (optional) A number, default 1 because that's the
                            only API version Twitter has now

            **params - You may pass items that are taken in this doc
                       (https://dev.twitter.com/docs/api/1/post/statuses/update_with_media)
        """
        url = 'https://upload.twitter.com/%d/statuses/update_with_media.json' % version
        return self._media_update(url,
                                  {'media': (file_, open(file_, 'rb'))},
                                  **params)

    def _media_update(self, url, file_, **params):
        return self.post(url, params=params, files=file_)

    def getProfileImageUrl(self, username, size='normal', version=1):
        """Gets the URL for the user's profile image.

            :param username: (required) Username, self explanatory.
            :param size: (optional) Default 'normal' (48px by 48px)
                            bigger - 73px by 73px
                            mini - 24px by 24px
                            original - undefined, be careful -- images may be
                                       large in bytes and/or size.
            :param version: A number, default 1 because that's the only API
                            version Twitter has now
        """
        endpoint = 'users/profile_image/%s' % username
        url = self.api_url % version + '/' + endpoint

        response = self.client.get(url, params={'size': size}, allow_redirects=False)
        image_url = response.headers.get('location')

        if response.status_code in (301, 302, 303, 307) and image_url is not None:
            return image_url
        else:
            raise TwythonError('getProfileImageUrl() threw an error.',
                                error_code=response.status_code)

    @staticmethod
    def stream(data, callback):
        """A Streaming API endpoint, because requests (by Kenneth Reitz)
            makes this not stupidly annoying to implement.

            In reality, Twython does absolutely *nothing special* here,
            but people new to programming expect this type of function to
            exist for this library, so we provide it for convenience.

            Seriously, this is nothing special. :)

            For the basic stream you're probably accessing, you'll want to
            pass the following as data dictionary keys. If you need to use
            OAuth (newer streams), passing secrets/etc
            as keys SHOULD work...

            This is all done over SSL (https://), so you're not left
            totally vulnerable by passing your password.

            :param username: (required) Username, self explanatory.
            :param password: (required) The Streaming API doesn't use OAuth,
                             so we do this the old school way.
            :param callback: (required) Callback function to be fired when
                             tweets come in (this is an event-based-ish API).
            :param endpoint: (optional) Override the endpoint you're using
                             with the Twitter Streaming API. This is defaulted
                             to the one that everyone has access to, but if
                             Twitter <3's you feel free to set this to your
                             wildest desires.
        """
        endpoint = 'https://stream.twitter.com/1/statuses/filter.json'
        if 'endpoint' in data:
            endpoint = data.pop('endpoint')

        needs_basic_auth = False
        if 'username' in data and 'password' in data:
            needs_basic_auth = True
            username = data.pop('username')
            password = data.pop('password')

        if needs_basic_auth:
            stream = requests.post(endpoint,
                                   data=data,
                                   auth=(username, password))
        else:
            stream = requests.post(endpoint, data=data)

        for line in stream.iter_lines():
            if line:
                try:
                    callback(simplejson.loads(line))
                except ValueError:
                    raise TwythonError('Response was not valid JSON, unable to decode.')

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
