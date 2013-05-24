from .. import __version__
from ..compat import json
from ..exceptions import TwythonStreamError
from .types import TwythonStreamerTypes

import requests
from requests_oauthlib import OAuth1

import time


class TwythonStreamer(object):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret,
                 timeout=300, retry_count=None, retry_in=10, headers=None):
        """Streaming class for a friendly streaming user experience

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
        :param headers: (optional) Custom headers to send along with the
                        request
        """

        self.auth = OAuth1(app_key, app_secret,
                           oauth_token, oauth_token_secret)

        self.headers = {'User-Agent': 'Twython Streaming v' + __version__}
        if headers:
            self.headers.update(headers)

        self.client = requests.Session()
        self.client.auth = self.auth
        self.client.headers = self.headers
        self.client.stream = True

        self.timeout = timeout

        self.api_version = '1.1'

        self.retry_in = retry_in
        self.retry_count = retry_count

        # Set up type methods
        StreamTypes = TwythonStreamerTypes(self)
        self.statuses = StreamTypes.statuses
        self.user = StreamTypes.user
        self.site = StreamTypes.site

        self.connected = False

    def _request(self, url, method='GET', params=None):
        """Internal stream request handling"""
        self.connected = True
        retry_counter = 0

        method = method.lower()
        func = getattr(self.client, method)

        def _send(retry_counter):
            while self.connected:
                try:
                    if method == 'get':
                        response = func(url, params=params, timeout=self.timeout)
                    else:
                        response = func(url, data=params, timeout=self.timeout)
                except requests.exceptions.Timeout:
                    self.on_timeout()
                else:
                    if response.status_code != 200:
                        self.on_error(response.status_code, response.content)

                    if self.retry_count and (self.retry_count - retry_counter) > 0:
                        time.sleep(self.retry_in)
                        retry_counter += 1
                        _send(retry_counter)

                    return response

        while self.connected:
            response = _send(retry_counter)

            for line in response.iter_lines():
                if not self.connected:
                    break
                if line:
                    try:
                        self.on_success(json.loads(line))
                    except ValueError:
                        raise TwythonStreamError('Response was not valid JSON, \
                                                  unable to decode.')

    def on_success(self, data):
        """Called when data has been successfull received from the stream

        Feel free to override this to handle your streaming data how you
        want it handled.
        See https://dev.twitter.com/docs/streaming-apis/messages for messages
        sent along in stream responses.

        :param data: dict of data recieved from the stream
        """

        if 'delete' in data:
            self.on_delete(data.get('delete'))
        elif 'limit' in data:
            self.on_limit(data.get('limit'))
        elif 'disconnect' in data:
            self.on_disconnect(data.get('disconnect'))

    def on_error(self, status_code, data):
        """Called when stream returns non-200 status code

        Feel free to override this to handle your streaming data how you
        want it handled.

        :param status_code: Non-200 status code sent from stream
        :param data: Error message sent from stream
        """
        return

    def on_delete(self, data):
        """Called when a deletion notice is received

        Feel free to override this to handle your streaming data how you
        want it handled.

        Twitter docs for deletion notices: http://spen.se/8qujd

        :param data: dict of data from the 'delete' key recieved from
                     the stream
        """
        return

    def on_limit(self, data):
        """Called when a limit notice is received

        Feel free to override this to handle your streaming data how you
        want it handled.

        Twitter docs for limit notices: http://spen.se/hzt0b

        :param data: dict of data from the 'limit' key recieved from
                     the stream
        """
        return

    def on_disconnect(self, data):
        """Called when a disconnect notice is received

        Feel free to override this to handle your streaming data how you
        want it handled.

        Twitter docs for disconnect notices: http://spen.se/xb6mm

        :param data: dict of data from the 'disconnect' key recieved from
                     the stream
        """
        return

    def on_timeout(self):
        return

    def disconnect(self):
        self.connected = False
