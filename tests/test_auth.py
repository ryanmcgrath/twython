from twython import Twython, TwythonError, TwythonAuthError

from .config import app_key, app_secret, screen_name

import unittest


class TwythonAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.api = Twython(app_key, app_secret)
        self.bad_api = Twython('BAD_APP_KEY', 'BAD_APP_SECRET')

        self.oauth2_api = Twython(app_key, app_secret, oauth_version=2)

    def test_get_authentication_tokens(self):
        """Test getting authentication tokens works"""
        self.api.get_authentication_tokens(callback_url='http://google.com/',
                                           force_login=True,
                                           screen_name=screen_name)

    def test_get_authentication_tokens_bad_tokens(self):
        """Test getting authentication tokens with bad tokens
        raises TwythonAuthError"""
        self.assertRaises(TwythonAuthError, self.bad_api.get_authentication_tokens,
                          callback_url='http://google.com/')

    def test_get_authorized_tokens_bad_tokens(self):
        """Test getting final tokens fails with wrong tokens"""
        self.assertRaises(TwythonError, self.bad_api.get_authorized_tokens,
                          'BAD_OAUTH_VERIFIER')

    def test_get_authentication_tokens_raises_error_when_oauth2(self):
        """Test when API is set for OAuth 2, get_authentication_tokens raises
        a TwythonError"""
        self.assertRaises(TwythonError, self.oauth2_api.get_authentication_tokens)

    def test_get_authorization_tokens_raises_error_when_oauth2(self):
        """Test when API is set for OAuth 2, get_authorized_tokens raises
        a TwythonError"""
        self.assertRaises(TwythonError, self.oauth2_api.get_authorized_tokens,
                          'BAD_OAUTH_VERIFIER')

    def test_obtain_access_token(self):
        """Test obtaining an Application Only OAuth 2 access token succeeds"""
        self.oauth2_api.obtain_access_token()

    def test_obtain_access_token_raises_error_when_oauth1(self):
        """Test when API is set for OAuth 1, obtain_access_token raises a
        TwythonError"""
        self.assertRaises(TwythonError, self.api.obtain_access_token)
