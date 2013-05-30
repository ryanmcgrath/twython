import re

import requests
from requests_oauthlib import OAuth1

from . import __version__
from .compat import json, urlencode, parse_qsl, quote_plus, str, is_py2
from .endpoints import api_table
from .exceptions import TwythonError, TwythonAuthError, TwythonRateLimitError
from .helpers import _transparent_params


class Twython(object):
    def __init__(self, app_key=None, app_secret=None, oauth_token=None,
                 oauth_token_secret=None, headers=None, proxies=None,
                 api_version='1.1', ssl_verify=True):
        """Instantiates an instance of Twython. Takes optional parameters for authentication and such (see below).

            :param app_key: (optional) Your applications key
            :param app_secret: (optional) Your applications secret key
            :param oauth_token: (optional) Used with oauth_token_secret to make authenticated calls
            :param oauth_token_secret: (optional) Used with oauth_token to make authenticated calls
            :param headers: (optional) Custom headers to send along with the request
            :param proxies: (optional) A dictionary of proxies, for example {"http":"proxy.example.org:8080", "https":"proxy.example.org:8081"}.
            :param ssl_verify: (optional) Turns off ssl verification when False. Useful if you have development server issues.
        """

        # API urls, OAuth urls and API version; needed for hitting that there API.
        self.api_version = api_version
        self.api_url = 'https://api.twitter.com/%s'
        self.request_token_url = self.api_url % 'oauth/request_token'
        self.access_token_url = self.api_url % 'oauth/access_token'
        self.authenticate_url = self.api_url % 'oauth/authenticate'

        self.app_key = app_key
        self.app_secret = app_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

        req_headers = {'User-Agent': 'Twython v' + __version__}
        if headers:
            req_headers.update(headers)

        # Generate OAuth authentication object for the request
        # If no keys/tokens are passed to __init__, auth=None allows for
        # unauthenticated requests, although I think all v1.1 requests need auth
        auth = None
        if self.app_key is not None and self.app_secret is not None and \
           self.oauth_token is None and self.oauth_token_secret is None:
            auth = OAuth1(self.app_key, self.app_secret)

        if self.app_key is not None and self.app_secret is not None and \
           self.oauth_token is not None and self.oauth_token_secret is not None:
            auth = OAuth1(self.app_key, self.app_secret,
                          self.oauth_token, self.oauth_token_secret)

        self.client = requests.Session()
        self.client.headers = req_headers
        self.client.proxies = proxies
        self.client.auth = auth
        self.client.verify = ssl_verify

        self._last_call = None

        def _setFunc(key):
            '''Register functions, attaching them to the Twython instance'''
            return lambda **kwargs: self._constructFunc(key, **kwargs)

        # Loop through all our Twitter API endpoints made available in endpoints.py
        for key in api_table.keys():
            self.__dict__[key] = _setFunc(key)

    def __repr__(self):
        return '<Twython: %s>' % (self.app_key)

    def _constructFunc(self, api_call, **kwargs):
        # Go through and replace any {{mustaches}} that are in our API url.
        fn = api_table[api_call]
        url = re.sub(
            '\{\{(?P<m>[a-zA-Z_]+)\}\}',
            lambda m: "%s" % kwargs.get(m.group(1)),
            self.api_url % self.api_version + fn['url']
        )

        return self._request(url, method=fn['method'], params=kwargs)

    def _request(self, url, method='GET', params=None, api_call=None):
        '''Internal response generator, no sense in repeating the same
        code twice, right? ;)
        '''
        method = method.lower()
        params = params or {}

        func = getattr(self.client, method)
        params, files = _transparent_params(params)
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

        #  Wrap the json loads in a try, and defer an error
        #  Twitter will return invalid json with an error code in the headers
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
            if errors and isinstance(errors, list):
                error_message = errors[0]['message']
            else:
                error_message = errors
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

    def request(self, endpoint, method='GET', params=None, version='1.1'):
        # In case they want to pass a full Twitter URL
        # i.e. https://api.twitter.com/1.1/search/tweets.json
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            url = endpoint
        else:
            url = '%s/%s.json' % (self.api_url % version, endpoint)

        content = self._request(url, method=method, params=params, api_call=url)

        return content

    def get(self, endpoint, params=None, version='1.1'):
        return self.request(endpoint, params=params, version=version)

    def post(self, endpoint, params=None, version='1.1'):
        return self.request(endpoint, 'POST', params=params, version=version)

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
        else:
            return None

    def get_authentication_tokens(self, callback_url=None, force_login=False, screen_name=''):
        """Returns a dict including an authorization URL (auth_url) to direct a user to

            :param callback_url: (optional) Url the user is returned to after they authorize your app (web clients only)
            :param force_login: (optional) Forces the user to enter their credentials to ensure the correct users account is authorized.
            :param app_secret: (optional) If forced_login is set OR user is not currently logged in, Prefills the username input box of the OAuth login screen with the given value
        """
        callback_url = callback_url or self.callback_url
        request_args = {}
        if callback_url:
            request_args['oauth_callback'] = callback_url
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

            :param oauth_verifier: (required) The oauth_verifier (or a.k.a PIN for non web apps) retrieved from the callback url querystring
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
    def construct_api_url(base_url, params=None):
        querystring = []
        params, _ = _transparent_params(params or {})
        params = requests.utils.to_key_val_list(params)
        for (k, v) in params:
            querystring.append(
                '%s=%s' % (Twython.encode(k), quote_plus(Twython.encode(v)))
            )
        return '%s?%s' % (base_url, '&'.join(querystring))

    def search_gen(self, search_query, **kwargs):
        """Returns a generator of tweets that match a specified query.

            Documentation: https://dev.twitter.com/docs/api/1.1/get/search/tweets

            e.g search = x.search_gen('python')
                for result in search:
                    print result
        """
        content = self.search(q=search_query, **kwargs)

        if not content.get('statuses'):
            raise StopIteration

        for tweet in content['statuses']:
            yield tweet

        try:
            if not 'since_id' in kwargs:
                kwargs['since_id'] = (int(content['statuses'][0]['id_str']) + 1)
        except (TypeError, ValueError):
            raise TwythonError('Unable to generate next page of search results, `page` is not a number.')

        for tweet in self.search_gen(search_query, **kwargs):
            yield tweet

    @staticmethod
    def unicode2utf8(text):
        try:
            if is_py2 and isinstance(text, str):
                text = text.encode('utf-8')
        except:
            pass
        return text

    @staticmethod
    def encode(text):
        if is_py2 and isinstance(text, (str)):
            return Twython.unicode2utf8(text)
        return str(text)
