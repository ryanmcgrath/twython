from twython import TwythonStreamer, TwythonStreamError

from .config import (
    app_key, app_secret, oauth_token, oauth_token_secret
)

import unittest


class TwythonStreamTestCase(unittest.TestCase):
    def setUp(self):
        class MyStreamer(TwythonStreamer):
            def on_success(self, data):
                self.disconnect()

            def on_error(self, status_code, data):
                raise TwythonStreamError(data)

        self.api = MyStreamer(app_key, app_secret,
                              oauth_token, oauth_token_secret)

    def test_stream_status_filter(self):
        self.api.statuses.filter(track='twitter')

    def test_stream_status_sample(self):
        self.api.statuses.sample()

    def test_stream_status_firehose(self):
        self.assertRaises(TwythonStreamError, self.api.statuses.firehose,
                          track='twitter')

    def test_stream_site(self):
        self.assertRaises(TwythonStreamError, self.api.site,
                          follow='twitter')

    def test_stream_user(self):
        self.api.user(track='twitter')
