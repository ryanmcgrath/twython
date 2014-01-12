from twython import Twython, TwythonError, TwythonAuthError

from .config import app_key, app_secret, screen_name, unittest


class TwythonAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.api = Twython(app_key, app_secret)
        self.bad_api = Twython('BAD_APP_KEY', 'BAD_APP_SECRET')
        self.bad_api_invalid_tokens = Twython('BAD_APP_KEY', 'BAD_APP_SECRET',
                                              'BAD_OT', 'BAD_OTS')

        self.oauth2_api = Twython(app_key, app_secret, oauth_version=2)
        self.oauth2_bad_api = Twython('BAD_APP_KEY', 'BAD_APP_SECRET',
                                      oauth_version=2)

    @unittest.skip('skipping non-updated test')
    def test_get_authentication_tokens(self):
        """Test getting authentication tokens works"""
        self.api.get_authentication_tokens(callback_url='http://google.com/',
                                           force_login=True,
                                           screen_name=screen_name)

    @unittest.skip('skipping non-updated test')
    def test_get_authentication_tokens_bad_tokens(self):
        """Test getting authentication tokens with bad tokens
        raises TwythonAuthError"""
        self.assertRaises(TwythonAuthError, self.bad_api.get_authentication_tokens,
                          callback_url='http://google.com/')

    @unittest.skip('skipping non-updated test')
    def test_get_authorized_tokens_bad_tokens(self):
        """Test getting final tokens fails with wrong tokens"""
        self.assertRaises(TwythonError, self.bad_api.get_authorized_tokens,
                          'BAD_OAUTH_VERIFIER')

    @unittest.skip('skipping non-updated test')
    def test_get_authorized_tokens_invalid_or_expired_tokens(self):
        """Test getting final token fails when invalid or expired tokens have been passed"""
        self.assertRaises(TwythonError, self.bad_api_invalid_tokens.get_authorized_tokens,
                         'BAD_OAUTH_VERIFIER')

    @unittest.skip('skipping non-updated test')
    def test_get_authentication_tokens_raises_error_when_oauth2(self):
        """Test when API is set for OAuth 2, get_authentication_tokens raises
        a TwythonError"""
        self.assertRaises(TwythonError, self.oauth2_api.get_authentication_tokens)

    @unittest.skip('skipping non-updated test')
    def test_get_authorization_tokens_raises_error_when_oauth2(self):
        """Test when API is set for OAuth 2, get_authorized_tokens raises
        a TwythonError"""
        self.assertRaises(TwythonError, self.oauth2_api.get_authorized_tokens,
                          'BAD_OAUTH_VERIFIER')

    @unittest.skip('skipping non-updated test')
    def test_obtain_access_token(self):
        """Test obtaining an Application Only OAuth 2 access token succeeds"""
        self.oauth2_api.obtain_access_token()

    @unittest.skip('skipping non-updated test')
    def test_obtain_access_token_bad_tokens(self):
        """Test obtaining an Application Only OAuth 2 access token using bad app tokens fails"""
        self.assertRaises(TwythonAuthError,
                          self.oauth2_bad_api.obtain_access_token)

    @unittest.skip('skipping non-updated test')
    def test_obtain_access_token_raises_error_when_oauth1(self):
        """Test when API is set for OAuth 1, obtain_access_token raises a
        TwythonError"""
        self.assertRaises(TwythonError, self.api.obtain_access_token)
