import re
import warnings

import requests
from requests_oauthlib import OAuth1

from .advisory import TwythonDeprecationWarning
from .compat import json, urlencode, parse_qsl, quote_plus
from .endpoints import api_table
from .exceptions import TwythonError, TwythonAuthError, TwythonRateLimitError
from .version import __version__

warnings.simplefilter('always', TwythonDeprecationWarning)  # For Python 2.7 >


class Twython(object):
    def __init__(self, app_key=None, app_secret=None, oauth_token=None,
                 oauth_token_secret=None, headers=None, proxies=None,
                 version='1.1', callback_url=None, ssl_verify=True,
                 twitter_token=None, twitter_secret=None):
        """Instantiates an instance of Twython. Takes optional parameters for authentication and such (see below).

            :param app_key: (optional) Your applications key
            :param app_secret: (optional) Your applications secret key
            :param oauth_token: (optional) Used with oauth_token_secret to make authenticated calls
            :param oauth_token_secret: (optional) Used with oauth_token to make authenticated calls
            :param headers: (optional) Custom headers to send along with the request
            :param callback_url: (optional) If set, will overwrite the callback url set in your application
            :param proxies: (optional) A dictionary of proxies, for example {"http":"proxy.example.org:8080", "https":"proxy.example.org:8081"}.
            :param ssl_verify: (optional) Turns off ssl verification when False. Useful if you have development server issues.
        """

        # API urls, OAuth urls and API version; needed for hitting that there API.
        self.api_version = version
        self.api_url = 'https://api.twitter.com/%s'
        self.request_token_url = self.api_url % 'oauth/request_token'
        self.access_token_url = self.api_url % 'oauth/access_token'
        self.authenticate_url = self.api_url % 'oauth/authenticate'

        self.app_key = app_key or twitter_token
        self.app_secret = app_secret or twitter_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

        self.callback_url = callback_url

        if twitter_token or twitter_secret:
            warnings.warn(
                'Instead of twitter_token or twitter_secret, please use app_key or app_secret (respectively).',
                TwythonDeprecationWarning,
                stacklevel=2
            )

        if callback_url:
            warnings.warn(
                'Please pass callback_url to the get_authentication_tokens method rather than Twython.__init__',
                TwythonDeprecationWarning,
                stacklevel=2
            )

        self.headers = {'User-Agent': 'Twython v' + __version__}
        if headers:
            self.headers.update(headers)

        # Generate OAuth authentication object for the request
        # If no keys/tokens are passed to __init__, self.auth=None allows for
        # unauthenticated requests, although I think all v1.1 requests need auth
        self.auth = None
        if self.app_key is not None and self.app_secret is not None and \
           self.oauth_token is None and self.oauth_token_secret is None:
            self.auth = OAuth1(self.app_key, self.app_secret)

        if self.app_key is not None and self.app_secret is not None and \
           self.oauth_token is not None and self.oauth_token_secret is not None:
            self.auth = OAuth1(self.app_key, self.app_secret,
                               self.oauth_token, self.oauth_token_secret)

        self.client = requests.Session()
        self.client.headers = self.headers
        self.client.proxies = proxies
        self.client.auth = self.auth
        self.client.verify = ssl_verify

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
            lambda m: "%s" % kwargs.get(m.group(1)),
            self.api_url % self.api_version + fn['url']
        )

        content = self._request(url, method=fn['method'], params=kwargs)

        return content

    def _request(self, url, method='GET', params=None, files=None, api_call=None):
        '''Internal response generator, no sense in repeating the same
        code twice, right? ;)
        '''
        method = method.lower()
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
            'headers': response.headers,
            'status_code': response.status_code,
            'url': response.url,
            'content': content,
        }

        #  wrap the json loads in a try, and defer an error
        #  why? twitter will return invalid json with an error code in the headers
        json_error = False
        try:
            try:
                # try to get json
                content = content.json()
            except AttributeError:
                # if unicode detected
                content = json.loads(content)
        except ValueError:
            json_error = True
            content = {}

        if response.status_code > 304:
            # If there is no error message, use a default.
            errors = content.get('errors',
                                 [{'message': 'An error occurred processing your request.'}])
            error_message = errors[0]['message']
            self._last_call['api_error'] = error_message

            ExceptionType = TwythonError
            if response.status_code == 429:
                # Twitter API 1.1, always return 429 when rate limit is exceeded
                ExceptionType = TwythonRateLimitError
            elif response.status_code == 401 or 'Bad Authentication data' in error_message:
                # Twitter API 1.1, returns a 401 Unauthorized or
                # a 400 "Bad Authentication data" for invalid/expired app keys/user tokens
                ExceptionType = TwythonAuthError

            raise ExceptionType(error_message,
                                error_code=response.status_code,
                                retry_after=response.headers.get('retry-after'))

        # if we have a json error here, then it's not an official Twitter API error
        if json_error and not response.status_code in (200, 201, 202):
            raise TwythonError('Response was not valid JSON, unable to decode.')

        return content

    '''
    # Dynamic Request Methods
    Just in case Twitter releases something in their API
    and a developer wants to implement it on their app, but
    we haven't gotten around to putting it in Twython yet. :)
    '''

    def request(self, endpoint, method='GET', params=None, files=None, version='1.1'):
        # In case they want to pass a full Twitter URL
        # i.e. https://search.twitter.com/
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            url = endpoint
        else:
            url = '%s/%s.json' % (self.api_url % version, endpoint)

        content = self._request(url, method=method, params=params, files=files, api_call=url)

        return content

    def get(self, endpoint, params=None, version='1.1'):
        return self.request(endpoint, params=params, version=version)

    def post(self, endpoint, params=None, files=None, version='1.1'):
        return self.request(endpoint, 'POST', params=params, files=files, version=version)

    # End Dynamic Request Methods

    def get_lastfunction_header(self, header):
        """Returns the header in the last function
            This must be called after an API call, as it returns header based
            information.

            This will return None if the header is not present

            Most useful for the following header information:
                x-rate-limit-limit
                x-rate-limit-remaining
                x-rate-limit-class
                x-rate-limit-reset
        """
        if self._last_call is None:
            raise TwythonError('This function must be called after an API call.  It delivers header information.')
        if header in self._last_call['headers']:
            return self._last_call['headers'][header]
        return self._last_call

    def get_authentication_tokens(self, callback_url=None, force_login=False, screen_name=''):
        """Returns a dict including an authorization URL (auth_url) to direct a user to

            :param callback_url: (optional.. for now) Url the user is returned to after they authorize your app
            :param force_login: (optional) Forces the user to enter their credentials to ensure the correct users account is authorized.
            :param app_secret: (optional) If forced_login is set OR user is not currently logged in, Prefills the username input box of the OAuth login screen with the given value
        """
        callback_url = callback_url or self.callback_url
        request_args = {'oauth_callback': callback_url}
        response = self.client.get(self.request_token_url, params=request_args)

        if response.status_code == 401:
            raise TwythonAuthError(response.content, error_code=response.status_code)
        elif response.status_code != 200:
            raise TwythonError(response.content, error_code=response.status_code)

        request_tokens = dict(parse_qsl(response.content.decode('utf-8')))
        if not request_tokens:
            raise TwythonError('Unable to decode request tokens.')

        oauth_callback_confirmed = request_tokens.get('oauth_callback_confirmed') == 'true'

        auth_url_params = {
            'oauth_token': request_tokens['oauth_token'],
        }

        if force_login:
            auth_url_params.update({
                'force_login': force_login,
                'screen_name': screen_name
            })

        # Use old-style callback argument if server didn't accept new-style
        if callback_url and not oauth_callback_confirmed:
            auth_url_params['oauth_callback'] = self.callback_url

        request_tokens['auth_url'] = self.authenticate_url + '?' + urlencode(auth_url_params)

        return request_tokens

    def get_authorized_tokens(self, oauth_verifier):
        """Returns authorized tokens after they go through the auth_url phase.

        :param oauth_verifier: (required) The oauth_verifier retrieved from the callback url querystring
        """
        response = self.client.get(self.access_token_url, params={'oauth_verifier': oauth_verifier})
        authorized_tokens = dict(parse_qsl(response.content.decode('utf-8')))
        if not authorized_tokens:
            raise TwythonError('Unable to decode authorized tokens.')

        return authorized_tokens

    # ------------------------------------------------------------------------------------------------------------------------
    # The following methods are all different in some manner or require special attention with regards to the Twitter API.
    # Because of this, we keep them separate from all the other endpoint definitions - ideally this should be change-able,
    # but it's not high on the priority list at the moment.
    # ------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def shortenURL(url_to_shorten, shortener='http://is.gd/create.php'):
        """Shortens url specified by url_to_shorten.
            Note: Twitter automatically shortens all URLs behind their own custom t.co shortener now,
                but we keep this here for anyone who was previously using it for alternative purposes. ;)

            :param url_to_shorten: (required) The URL to shorten
            :param shortener: (optional) In case you want to use a different
                              URL shortening service
        """
        warnings.warn(
            'With requests it\'s easy enough for a developer to implement url shortenting themselves. Please see: https://github.com/ryanmcgrath/twython/issues/184',
            TwythonDeprecationWarning,
            stacklevel=2
        )

        if shortener == '':
            raise TwythonError('Please provide a URL shortening service.')

        request = requests.get(shortener, params={
            'format': 'json',
            'url': url_to_shorten
        })

        if request.status_code in [301, 201, 200]:
            return request.text
        else:
            raise TwythonError('shortenURL() failed with a %s error code.' % request.status_code)

    @staticmethod
    def constructApiURL(base_url, params):
        return base_url + '?' + '&'.join(['%s=%s' % (Twython.unicode2utf8(key), quote_plus(Twython.unicode2utf8(value))) for (key, value) in params.iteritems()])

    def searchGen(self, search_query, **kwargs):
        """ Returns a generator of tweets that match a specified query.

            Documentation: https://dev.twitter.com/doc/get/search

            See Twython.search() for acceptable parameters

            e.g search = x.searchGen('python')
                for result in search:
                    print result
        """
        kwargs['q'] = search_query
        content = self.search(q=search_query, **kwargs)

        if not content['results']:
            raise StopIteration

        for tweet in content['results']:
            yield tweet

        try:
            kwargs['page'] = 2 if not 'page' in kwargs else (int(kwargs['page']) + 1)
        except (TypeError, ValueError):
            raise TwythonError('Unable to generate next page of search results, `page` is not a number.')

        for tweet in self.searchGen(search_query, **kwargs):
            yield tweet

    # The following methods are apart from the other Account methods,
    # because they rely on a whole multipart-data posting function set.

    ## Media Uploading functions ##############################################

    def updateProfileBackgroundImage(self, file_, version='1.1', **params):
        """Updates the authenticating user's profile background image.

            :param file_: (required) A string to the location of the file
                          (less than 800KB in size, larger than 2048px width will scale down)
            :param version: (optional) A number, default 1.1 because that's the
                            current API version for Twitter (Legacy = 1)

            **params - You may pass items that are stated in this doc
                       (https://dev.twitter.com/docs/api/1.1/post/account/update_profile_background_image)
        """

        return self.post('account/update_profile_background_image',
                         params=params,
                         files={'image': (file_, open(file_, 'rb'))},
                         version=version)

    def updateProfileImage(self, file_, version='1.1', **params):
        """Updates the authenticating user's profile image (avatar).

            :param file_: (required) A string to the location of the file
            :param version: (optional) A number, default 1.1 because that's the
                            current API version for Twitter (Legacy = 1)

            **params - You may pass items that are stated in this doc
                       (https://dev.twitter.com/docs/api/1.1/post/account/update_profile_image)
        """

        return self.post('account/update_profile_image',
                         params=params,
                         files={'image': (file_, open(file_, 'rb'))},
                         version=version)

    def updateStatusWithMedia(self, file_, version='1.1', **params):
        """Updates the users status with media

            :param file_: (required) A string to the location of the file
            :param version: (optional) A number, default 1.1 because that's the
                            current API version for Twitter (Legacy = 1)

            **params - You may pass items that are taken in this doc
                       (https://dev.twitter.com/docs/api/1.1/post/statuses/update_with_media)
        """

        return self.post('statuses/update_with_media',
                         params=params,
                         files={'media': (file_, open(file_, 'rb'))},
                         version=version)

    def updateProfileBannerImage(self, file_, version='1.1', **params):
        """Updates the users profile banner

            :param file_: (required) A string to the location of the file
            :param version: (optional) A number, default 1 because that's the
                            only API version for Twitter that supports this call

            **params - You may pass items that are taken in this doc
                       (https://dev.twitter.com/docs/api/1.1/post/account/update_profile_banner)
        """

        return self.post('account/update_profile_banner',
                         params=params,
                         files={'banner': (file_, open(file_, 'rb'))},
                         version=version)

    ###########################################################################

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
                    callback(json.loads(line))
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
