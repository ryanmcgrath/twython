from twython import TwythonStreamer, TwythonStreamError

from .config import (
    app_key, app_secret, oauth_token, oauth_token_secret, unittest
)


class TwythonStreamTestCase(unittest.TestCase):
    def setUp(self):
        class MyStreamer(TwythonStreamer):
            def on_success(self, data):
                self.disconnect()

            def on_error(self, status_code, data):
                raise TwythonStreamError(data)

        self.api = MyStreamer(app_key, app_secret,
                              oauth_token, oauth_token_secret)

        client_args = {
            'headers': {
                'User-Agent': '__twython__ Stream Test'
            }
        }
        # Initialize with header for coverage checking for User-Agent
        self.api_with_header = MyStreamer(app_key, app_secret,
                                          oauth_token, oauth_token_secret,
                                          client_args=client_args)

    @unittest.skip('skipping non-updated test')
    def test_stream_status_filter(self):
        self.api.statuses.filter(track='twitter')

    @unittest.skip('skipping non-updated test')
    def test_stream_status_sample(self):
        self.api.statuses.sample()

    @unittest.skip('skipping non-updated test')
    def test_stream_status_firehose(self):
        self.assertRaises(TwythonStreamError, self.api.statuses.firehose,
                          track='twitter')

    @unittest.skip('skipping non-updated test')
    def test_stream_site(self):
        self.assertRaises(TwythonStreamError, self.api.site,
                          follow='twitter')

    @unittest.skip('skipping non-updated test')
    def test_stream_user(self):
        self.api.user(track='twitter')
