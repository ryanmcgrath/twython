# -*- coding: utf-8 -*-

"""
twython.streaming.api
~~~~~~~~~~~~~~~~~~~~~

This module contains functionality for interfacing with streaming
Twitter API calls.
"""

from .. import __version__
from ..compat import json, is_py3
from ..helpers import _transparent_params
from .types import TwythonStreamerTypes

import requests
from requests_oauthlib import OAuth1

import time


class TwythonStreamer(object):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret,
                 timeout=300, retry_count=None, retry_in=10, client_args=None,
                 handlers=None, chunk_size=1):
        """Streaming class for a friendly streaming user experience
        Authentication IS required to use the Twitter Streaming API

        :param app_key: (required) Your applications key
        :param app_secret: (required) Your applications secret key
        :param oauth_token: (required) Used with oauth_token_secret to make
                            authenticated calls
        :param oauth_token_secret: (required) Used with oauth_token to make
                                   authenticated calls
        :param timeout: (optional) How long (in secs) the streamer should wait
                        for a response from Twitter Streaming API
        :param retry_count: (optional) Number of times the API call should be
                            retired
        :param retry_in: (optional) Amount of time (in secs) the previous
                         API call should be tried again
        :param client_args: (optional) Accepts some requests Session
                            parameters and some requests Request parameters.
                            See
                            http://docs.python-requests.org/en/latest/api/#sessionapi
                            and requests section below it for details.
                            [ex. headers, proxies, verify(SSL verification)]
        :param handlers: (optional) Array of message types for which
                         corresponding handlers will be called

        :param chunk_size: (optional) Define the buffer size before data is
                           actually returned from the Streaming API. Default: 1
        """

        self.auth = OAuth1(app_key, app_secret,
                           oauth_token, oauth_token_secret)

        self.client_args = client_args or {}
        default_headers = {'User-Agent': 'Twython Streaming v' + __version__}
        if 'headers' not in self.client_args:
            # If they didn't set any headers, set our defaults for them
            self.client_args['headers'] = default_headers
        elif 'User-Agent' not in self.client_args['headers']:
            # If they set headers, but didn't include User-Agent..
            # set it for them
            self.client_args['headers'].update(default_headers)
        self.client_args['timeout'] = timeout

        self.client = requests.Session()
        self.client.auth = self.auth
        self.client.stream = True

        # Make a copy of the client args and iterate over them
        # Pop out all the acceptable args at this point because they will
        # Never be used again.
        client_args_copy = self.client_args.copy()
        for k, v in client_args_copy.items():
            if k in ('cert', 'headers', 'hooks', 'max_redirects', 'proxies'):
                setattr(self.client, k, v)
                self.client_args.pop(k)  # Pop, pop!

        self.api_version = '1.1'

        self.retry_in = retry_in
        self.retry_count = retry_count

        # Set up type methods
        StreamTypes = TwythonStreamerTypes(self)
        self.statuses = StreamTypes.statuses
        self.user = StreamTypes.user
        self.site = StreamTypes.site

        self.connected = False

        self.handlers = handlers if handlers else \
            ['delete', 'limit', 'disconnect']

        self.chunk_size = chunk_size

    def _request(self, url, method='GET', params=None):
        """Internal stream request handling"""
        self.connected = True
        retry_counter = 0

        method = method.lower()
        func = getattr(self.client, method)
        params, _ = _transparent_params(params)

        def _send(retry_counter):
            requests_args = {}
            for k, v in self.client_args.items():
                # Maybe this should be set as a class
                # variable and only done once?
                if k in ('timeout', 'allow_redirects', 'verify'):
                    requests_args[k] = v

            while self.connected:
                try:
                    if method == 'get':
                        requests_args['params'] = params
                    else:
                        requests_args['data'] = params

                    response = func(url, **requests_args)
                except requests.exceptions.Timeout:
                    self.on_timeout()
                else:
                    if response.status_code != 200:
                        self.on_error(response.status_code, response.content)

                    if self.retry_count and \
                       (self.retry_count - retry_counter) > 0:
                        time.sleep(self.retry_in)
                        retry_counter += 1
                        _send(retry_counter)

                    return response

        while self.connected:
            response = _send(retry_counter)

            for line in response.iter_lines(self.chunk_size):
                if not self.connected:
                    break
                if line:
                    try:
                        if is_py3:
                            line = line.decode('utf-8')
                        data = json.loads(line)
                    except ValueError:  # pragma: no cover
                        self.on_error(response.status_code,
                                      'Unable to decode response, \
                                      not valid JSON.')
                    else:
                        if self.on_success(data):  # pragma: no cover
                            for message_type in self.handlers:
                                if message_type in data:
                                    handler = getattr(self,
                                                      'on_' + message_type,
                                                      None)
                                    if handler \
                                       and callable(handler) \
                                       and not handler(data.get(message_type)):
                                        break

        response.close()

    def on_success(self, data):  # pragma: no cover
        """Called when data has been successfully received from the stream.
        Returns True if other handlers for this message should be invoked.

        Feel free to override this to handle your streaming data how you
        want it handled. See
        https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/streaming-message-types
        for messages sent along in stream responses.

        :param data: data recieved from the stream
        :type data: dict
        """
        return True

    def on_error(self, status_code, data):  # pragma: no cover
        """Called when stream returns non-200 status code

        Feel free to override this to handle your streaming data how you
        want it handled.

        :param status_code: Non-200 status code sent from stream
        :type status_code: int

        :param data: Error message sent from stream
        :type data: dict
        """
        return

    def on_timeout(self):  # pragma: no cover
        """ Called when the request has timed out """
        return

    def disconnect(self):
        """Used to disconnect the streaming client manually"""
        self.connected = False
