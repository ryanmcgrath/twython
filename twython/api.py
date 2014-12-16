# -*- coding: utf-8 -*-

"""
twython.api
~~~~~~~~~~~

This module contains functionality for access to core Twitter API calls,
Twitter Authentication, and miscellaneous methods that are useful when
dealing with the Twitter API
"""

import warnings

import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1, OAuth2

from . import __version__
from .advisory import TwythonDeprecationWarning
from .compat import json, urlencode, parse_qsl, quote_plus, str, is_py2
from .endpoints import EndpointsMixin
from .exceptions import TwythonError, TwythonAuthError, TwythonRateLimitError
from .helpers import _transparent_params

warnings.simplefilter('always', TwythonDeprecationWarning)  # For Python 2.7 >


class Twython(EndpointsMixin, object):
    def __init__(self, app_key=None, app_secret=None, oauth_token=None,
                 oauth_token_secret=None, access_token=None,
                 token_type='bearer', oauth_version=1, api_version='1.1',
                 client_args=None, auth_endpoint='authenticate'):
        """Instantiates an instance of Twython. Takes optional parameters for
        authentication and such (see below).

        :param app_key: (optional) Your applications key
        :param app_secret: (optional) Your applications secret key
        :param oauth_token: (optional) When using **OAuth 1**, combined with
        oauth_token_secret to make authenticated calls
        :param oauth_token_secret: (optional) When using **OAuth 1** combined
        with oauth_token to make authenticated calls
        :param access_token: (optional) When using **OAuth 2**, provide a
        valid access token if you have one
        :param token_type: (optional) When using **OAuth 2**, provide your
        token type. Default: bearer
        :param oauth_version: (optional) Choose which OAuth version to use.
        Default: 1
        :param api_version: (optional) Choose which Twitter API version to
        use. Default: 1.1

        :param client_args: (optional) Accepts some requests Session parameters
        and some requests Request parameters.
              See http://docs.python-requests.org/en/latest/api/#sessionapi
              and requests section below it for details.
              [ex. headers, proxies, verify(SSL verification)]
        :param auth_endpoint: (optional) Lets you select which authentication
        endpoint will use your application.
              This will allow the application to have DM access
              if the endpoint is 'authorize'.
                Default: authenticate.
        """

        # API urls, OAuth urls and API version; needed for hitting that there
        # API.
        self.api_version = api_version
        self.api_url = 'https://api.twitter.com/%s'

        self.app_key = app_key
        self.app_secret = app_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.access_token = access_token

        # OAuth 1
        self.request_token_url = self.api_url % 'oauth/request_token'
        self.access_token_url = self.api_url % 'oauth/access_token'
        self.authenticate_url = self.api_url % ('oauth/%s' % auth_endpoint)

        if self.access_token:  # If they pass an access token, force OAuth 2
            oauth_version = 2

        self.oauth_version = oauth_version

        # OAuth 2
        if oauth_version == 2:
            self.request_token_url = self.api_url % 'oauth2/token'

        self.client_args = client_args or {}
        default_headers = {'User-Agent': 'Twython v' + __version__}
        if 'headers' not in self.client_args:
            # If they didn't set any headers, set our defaults for them
            self.client_args['headers'] = default_headers
        elif 'User-Agent' not in self.client_args['headers']:
            # If they set headers, but didn't include User-Agent.. set
            # it for them
            self.client_args['headers'].update(default_headers)

        # Generate OAuth authentication object for the request
        # If no keys/tokens are passed to __init__, auth=None allows for
        # unauthenticated requests, although I think all v1.1 requests
        # need auth
        auth = None
        if oauth_version == 1:
            # User Authentication is through OAuth 1
            if self.app_key is not None and self.app_secret is not None and \
               self.oauth_token is None and self.oauth_token_secret is None:
                auth = OAuth1(self.app_key, self.app_secret)

            if self.app_key is not None and self.app_secret is not None and \
               self.oauth_token is not None and self.oauth_token_secret is \
               not None:
                auth = OAuth1(self.app_key, self.app_secret,
                              self.oauth_token, self.oauth_token_secret)
        elif oauth_version == 2 and self.access_token:
            # Application Authentication is through OAuth 2
            token = {'token_type': token_type,
                     'access_token': self.access_token}
            auth = OAuth2(self.app_key, token=token)

        self.client = requests.Session()
        self.client.auth = auth

        # Make a copy of the client args and iterate over them
        # Pop out all the acceptable args at this point because they will
        # Never be used again.
        client_args_copy = self.client_args.copy()
        for k, v in client_args_copy.items():
            if k in ('cert', 'hooks', 'max_redirects', 'proxies'):
                setattr(self.client, k, v)
                self.client_args.pop(k)  # Pop, pop!

        # Headers are always present, so we unconditionally pop them and merge
        # them into the session headers.
        self.client.headers.update(self.client_args.pop('headers'))

        self._last_call = None

    def __repr__(self):
        return '<Twython: %s>' % (self.app_key)

    def _request(self, url, method='GET', params=None, api_call=None):
        """Internal request method"""
        method = method.lower()
        params = params or {}

        func = getattr(self.client, method)
        params, files = _transparent_params(params)

        requests_args = {}
        for k, v in self.client_args.items():
            # Maybe this should be set as a class variable and only done once?
            if k in ('timeout', 'allow_redirects', 'stream', 'verify'):
                requests_args[k] = v

        if method == 'get':
            requests_args['params'] = params
        else:
            requests_args.update({
                'data': params,
                'files': files,
            })
        try:
            response = func(url, **requests_args)
        except requests.RequestException as e:
            raise TwythonError(str(e))

        # create stash for last function intel
        self._last_call = {
            'api_call': api_call,
            'api_error': None,
            'cookies': response.cookies,
            'headers': response.headers,
            'status_code': response.status_code,
            'url': response.url,
            'content': response.text,
        }

        # greater than 304 (not modified) is an error
        if response.status_code > 304:
            error_message = self._get_error_message(response)
            self._last_call['api_error'] = error_message

            ExceptionType = TwythonError
            if response.status_code == 429:
                # Twitter API 1.1, always return 429 when
                # rate limit is exceeded
                ExceptionType = TwythonRateLimitError
            elif response.status_code == 401 or 'Bad Authentication data' \
                    in error_message:
                # Twitter API 1.1, returns a 401 Unauthorized or
                # a 400 "Bad Authentication data" for invalid/expired
                # app keys/user tokens
                ExceptionType = TwythonAuthError

            raise ExceptionType(
                error_message,
                error_code=response.status_code,
                retry_after=response.headers.get('X-Rate-Limit-Reset'))

        try:
            content = response.json()
        except ValueError:
            raise TwythonError('Response was not valid JSON. \
                               Unable to decode.')

        return content

    def _get_error_message(self, response):
        """Parse and return the first error message"""

        error_message = 'An error occurred processing your request.'
        try:
            content = response.json()
            # {"errors":[{"code":34,"message":"Sorry,
            # that page does not exist"}]}
            error_message = content['errors'][0]['message']
        except TypeError:
            error_message = content['errors']
        except ValueError:
            # bad json data from Twitter for an error
            pass
        except (KeyError, IndexError):
            # missing data so fallback to default message
            pass

        return error_message

    def request(self, endpoint, method='GET', params=None, version='1.1'):
        """Return dict of response received from Twitter's API

        :param endpoint: (required) Full url or Twitter API endpoint
                         (e.g. search/tweets)
        :type endpoint: string
        :param method: (optional) Method of accessing data, either
                       GET or POST. (default GET)
        :type method: string
        :param params: (optional) Dict of parameters (if any) accepted
                       the by Twitter API endpoint you are trying to
                       access (default None)
        :type params: dict or None
        :param version: (optional) Twitter API version to access
                        (default 1.1)
        :type version: string

        :rtype: dict
        """

        if endpoint.startswith('http://'):
            raise TwythonError('api.twitter.com is restricted to SSL/TLS traffic.')

        # In case they want to pass a full Twitter URL
        # i.e. https://api.twitter.com/1.1/search/tweets.json
        if endpoint.startswith('https://'):
            url = endpoint
        else:
            url = '%s/%s.json' % (self.api_url % version, endpoint)

        content = self._request(url, method=method, params=params,
                                api_call=url)

        return content

    def get(self, endpoint, params=None, version='1.1'):
        """Shortcut for GET requests via :class:`request`"""
        return self.request(endpoint, params=params, version=version)

    def post(self, endpoint, params=None, version='1.1'):
        """Shortcut for POST requests via :class:`request`"""
        return self.request(endpoint, 'POST', params=params, version=version)

    def get_lastfunction_header(self, header, default_return_value=None):
        """Returns a specific header from the last API call
        This will return None if the header is not present

        :param header: (required) The name of the header you want to get
                       the value of

        Most useful for the following header information:
            x-rate-limit-limit,
            x-rate-limit-remaining,
            x-rate-limit-class,
            x-rate-limit-reset

        """
        if self._last_call is None:
            raise TwythonError('This function must be called after an API call. \
                               It delivers header information.')

        return self._last_call['headers'].get(header, default_return_value)

    def get_authentication_tokens(self, callback_url=None, force_login=False,
                                  screen_name=''):
        """Returns a dict including an authorization URL, ``auth_url``, to
           direct a user to

        :param callback_url: (optional) Url the user is returned to after
                             they authorize your app (web clients only)
        :param force_login: (optional) Forces the user to enter their
                            credentials to ensure the correct users
                            account is authorized.
        :param screen_name: (optional) If forced_login is set OR user is
                            not currently logged in, Prefills the username
                            input box of the OAuth login screen with the
                            given value

        :rtype: dict
        """
        if self.oauth_version != 1:
            raise TwythonError('This method can only be called when your \
                               OAuth version is 1.0.')

        request_args = {}
        if callback_url:
            request_args['oauth_callback'] = callback_url
        response = self.client.get(self.request_token_url, params=request_args)

        if response.status_code == 401:
            raise TwythonAuthError(response.content,
                                   error_code=response.status_code)
        elif response.status_code != 200:
            raise TwythonError(response.content,
                               error_code=response.status_code)

        request_tokens = dict(parse_qsl(response.content.decode('utf-8')))
        if not request_tokens:
            raise TwythonError('Unable to decode request tokens.')

        oauth_callback_confirmed = request_tokens.get('oauth_callback_confirmed') \
            == 'true'

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

        request_tokens['auth_url'] = self.authenticate_url + \
            '?' + urlencode(auth_url_params)

        return request_tokens

    def get_authorized_tokens(self, oauth_verifier):
        """Returns a dict of authorized tokens after they go through the
        :class:`get_authentication_tokens` phase.

        :param oauth_verifier: (required) The oauth_verifier (or a.k.a PIN
        for non web apps) retrieved from the callback url querystring
        :rtype: dict

        """
        if self.oauth_version != 1:
            raise TwythonError('This method can only be called when your \
                               OAuth version is 1.0.')

        response = self.client.get(self.access_token_url,
                                   params={'oauth_verifier': oauth_verifier},
                                   headers={'Content-Type': 'application/\
                                   json'})

        if response.status_code == 401:
            try:
                try:
                    # try to get json
                    content = response.json()
                except AttributeError:  # pragma: no cover
                    # if unicode detected
                    content = json.loads(response.content)
            except ValueError:
                content = {}

            raise TwythonError(content.get('error', 'Invalid / expired To \
            ken'), error_code=response.status_code)

        authorized_tokens = dict(parse_qsl(response.content.decode('utf-8')))
        if not authorized_tokens:
            raise TwythonError('Unable to decode authorized tokens.')

        return authorized_tokens  # pragma: no cover

    def obtain_access_token(self):
        """Returns an OAuth 2 access token to make OAuth 2 authenticated
        read-only calls.

        :rtype: string
        """
        if self.oauth_version != 2:
            raise TwythonError('This method can only be called when your \
                               OAuth version is 2.0.')

        data = {'grant_type': 'client_credentials'}
        basic_auth = HTTPBasicAuth(self.app_key, self.app_secret)
        try:
            response = self.client.post(self.request_token_url,
                                        data=data, auth=basic_auth)
            content = response.content.decode('utf-8')
            try:
                content = content.json()
            except AttributeError:
                content = json.loads(content)
                access_token = content['access_token']
        except (KeyError, ValueError, requests.exceptions.RequestException):
            raise TwythonAuthError('Unable to obtain OAuth 2 access token.')
        else:
            return access_token

    @staticmethod
    def construct_api_url(api_url, **params):
        """Construct a Twitter API url, encoded, with parameters

        :param api_url: URL of the Twitter API endpoint you are attempting
        to construct
        :param \*\*params: Parameters that are accepted by Twitter for the
        endpoint you're requesting
        :rtype: string

        Usage::

          >>> from twython import Twython
          >>> twitter = Twython()

          >>> api_url = 'https://api.twitter.com/1.1/search/tweets.json'
          >>> constructed_url = twitter.construct_api_url(api_url, q='python',
          result_type='popular')
          >>> print constructed_url
          https://api.twitter.com/1.1/search/tweets.json?q=python&result_type=popular

        """
        querystring = []
        params, _ = _transparent_params(params or {})
        params = requests.utils.to_key_val_list(params)
        for (k, v) in params:
            querystring.append(
                '%s=%s' % (Twython.encode(k), quote_plus(Twython.encode(v)))
            )
        return '%s?%s' % (api_url, '&'.join(querystring))

    def search_gen(self, search_query, **params):  # pragma: no cover
        warnings.warn(
            'This method is deprecated. You should use Twython.cursor instead. \
            [eg. Twython.cursor(Twython.search, q=\'your_query\')]',
            TwythonDeprecationWarning,
            stacklevel=2
        )
        return self.cursor(self.search, q=search_query, **params)

    def cursor(self, function, return_pages=False, **params):
        """Returns a generator for results that match a specified query.

        :param function: Instance of a Twython function
        (Twython.get_home_timeline, Twython.search)
        :param \*\*params: Extra parameters to send with your request
        (usually parameters accepted by the Twitter API endpoint)
        :rtype: generator

        Usage::

          >>> from twython import Twython
          >>> twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN,
          OAUTH_TOKEN_SECRET)

          >>> results = twitter.cursor(twitter.search, q='python')
          >>> for result in results:
          >>>   print result

        """
        if not hasattr(function, 'iter_mode'):
            raise TwythonError('Unable to create generator for Twython \
                               method "%s"' % function.__name__)

        while True:
            content = function(**params)

            if not content:
                raise StopIteration

            if hasattr(function, 'iter_key'):
                results = content.get(function.iter_key)
            else:
                results = content

            if return_pages:
                yield results
            else:
                for result in results:
                    yield result

            if function.iter_mode == 'cursor' and \
               content['next_cursor_str'] == '0':
                raise StopIteration

            try:
                if function.iter_mode == 'id':
                    if 'max_id' not in params:
                        # Add 1 to the id because since_id and
                        # max_id are inclusive
                        if hasattr(function, 'iter_metadata'):
                            since_id = content[function.iter_metadata].get('since_id_str')
                        else:
                            since_id = content[0]['id_str']
                        params['since_id'] = (int(since_id) - 1)
                elif function.iter_mode == 'cursor':
                    params['cursor'] = content['next_cursor_str']
            except (TypeError, ValueError):  # pragma: no cover
                raise TwythonError('Unable to generate next page of search \
                                   results, `page` is not a number.')

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

    @staticmethod
    def html_for_tweet(tweet, use_display_url=True, use_expanded_url=False):
        """Return HTML for a tweet (urls, mentions, hashtags replaced with links)

        :param tweet: Tweet object from received from Twitter API
        :param use_display_url: Use display URL to represent link
        (ex. google.com, github.com). Default: True
        :param use_expanded_url: Use expanded URL to represent link
        (e.g. http://google.com). Default False

        If use_expanded_url is True, it overrides use_display_url.
        If use_display_url and use_expanded_url is False, short url will
        be used (t.co/xxxxx)

        """
        if 'retweeted_status' in tweet:
            tweet = tweet['retweeted_status']

        if 'entities' in tweet:
            text = tweet['text']
            entities = tweet['entities']

            # Mentions
            for entity in entities['user_mentions']:
                start, end = entity['indices'][0], entity['indices'][1]

                mention_html = '<a href="https://twitter.com/%(screen_name)s" class="twython-mention">@%(screen_name)s</a>'
                text = text.replace(tweet['text'][start:end],
                        mention_html % {'screen_name': entity['screen_name']})

            # Hashtags
            for entity in entities['hashtags']:
                start, end = entity['indices'][0], entity['indices'][1]

                hashtag_html = '<a href="https://twitter.com/search?q=%%23%(hashtag)s" class="twython-hashtag">#%(hashtag)s</a>'
                text = text.replace(tweet['text'][start:end], hashtag_html % {'hashtag': entity['text']})

            # Urls
            for entity in entities['urls']:
                start, end = entity['indices'][0], entity['indices'][1]
                if use_display_url and entity.get('display_url') \
                   and not use_expanded_url:
                    shown_url = entity['display_url']
                elif use_expanded_url and entity.get('expanded_url'):
                    shown_url = entity['expanded_url']
                else:
                    shown_url = entity['url']

                url_html = '<a href="%s" class="twython-url">%s</a>'
                text = text.replace(tweet['text'][start:end],
                                    url_html % (entity['url'], shown_url))

             # Media
            if 'media' in entities:
                for entity in entities['media']:
                    start, end = entity['indices'][0], entity['indices'][1]
                    if use_display_url and entity.get('display_url') \
                       and not use_expanded_url:
                        shown_url = entity['display_url']
                    elif use_expanded_url and entity.get('expanded_url'):
                        shown_url = entity['expanded_url']
                    else:
                        shown_url = entity['url']

                    url_html = '<a href="%s" class="twython-media">%s</a>'
                    text = text.replace(tweet['text'][start:end],
                                        url_html % (entity['url'], shown_url))

        return text
