# -*- coding: utf-8 -*-
from twython import Twython, TwythonError, TwythonAuthError, TwythonRateLimitError

from .config import (
    test_tweet_object, test_tweet_html, test_tweet_symbols_object,
    test_tweet_compat_object, test_tweet_extended_object, test_tweet_extended_html,
    unittest
)

import responses
import requests

from twython.compat import is_py2
if is_py2:
    from StringIO import StringIO
else:
    from io import StringIO

try:
    import unittest.mock as mock
except ImportError:
    import mock


class TwythonAPITestCase(unittest.TestCase):
    def setUp(self):
        self.api = Twython('', '', '', '')

    def get_url(self, endpoint):
        """Convenience function for mapping from endpoint to URL"""
        return '%s/%s.json' % (self.api.api_url % self.api.api_version, endpoint)

    def register_response(self, method, url, body='{}', match_querystring=False,
                          status=200, adding_headers=None, stream=False,
                          content_type='application/json; charset=utf-8'):
        """Wrapper function for responses for simpler unit tests"""

        # responses uses BytesIO to hold the body so it needs to be in bytes
        if not is_py2:
            body = bytes(body, 'UTF-8')

        responses.add(method, url, body, match_querystring,
                      status, adding_headers, stream, content_type)

    @responses.activate
    def test_request_should_handle_full_endpoint(self):
        """Test that request() accepts a full URL for the endpoint argument"""
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        self.register_response(responses.GET, url)

        self.api.request(url)

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(url, responses.calls[0].request.url)

    @responses.activate
    def test_request_should_handle_relative_endpoint(self):
        """Test that request() accepts a twitter endpoint name for the endpoint argument"""
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        self.register_response(responses.GET, url)

        self.api.request('search/tweets', version='1.1')

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(url, responses.calls[0].request.url)

    @responses.activate
    def test_request_should_post_request_regardless_of_case(self):
        """Test that request() accepts the HTTP method name regardless of case"""
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        self.register_response(responses.POST, url)

        self.api.request(url, method='POST')
        self.api.request(url, method='post')

        self.assertEqual(2, len(responses.calls))
        self.assertEqual('POST', responses.calls[0].request.method)
        self.assertEqual('POST', responses.calls[1].request.method)

    @responses.activate
    def test_request_should_throw_exception_with_invalid_http_method(self):
        """Test that request() throws an exception when an invalid HTTP method is passed"""
        # TODO(cash): should Twython catch the AttributeError and throw a TwythonError
        self.assertRaises(AttributeError, self.api.request, endpoint='search/tweets', method='INVALID')

    @responses.activate
    def test_request_should_encode_boolean_as_lowercase_string(self):
        """Test that request() encodes a boolean parameter as a lowercase string"""
        endpoint = 'search/tweets'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url)

        self.api.request(endpoint, params={'include_entities': True})
        self.api.request(endpoint, params={'include_entities': False})

        self.assertEqual(url + '?include_entities=true', responses.calls[0].request.url)
        self.assertEqual(url + '?include_entities=false', responses.calls[1].request.url)

    @responses.activate
    def test_request_should_handle_string_or_number_parameter(self):
        """Test that request() encodes a numeric or string parameter correctly"""
        endpoint = 'search/tweets'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url)

        self.api.request(endpoint, params={'lang': 'es'})
        self.api.request(endpoint, params={'count': 50})

        self.assertEqual(url + '?lang=es', responses.calls[0].request.url)
        self.assertEqual(url + '?count=50', responses.calls[1].request.url)

    @responses.activate
    def test_request_should_encode_list_of_strings_as_string(self):
        """Test that request() encodes a list of strings as a comma-separated string"""
        endpoint = 'search/tweets'
        url = self.get_url(endpoint)
        location = ['37.781157', '-122.39872', '1mi']
        self.register_response(responses.GET, url)

        self.api.request(endpoint, params={'geocode': location})

        # requests url encodes the parameters so , is %2C
        self.assertEqual(url + '?geocode=37.781157%2C-122.39872%2C1mi', responses.calls[0].request.url)

    @responses.activate
    def test_request_should_encode_numeric_list_as_string(self):
        """Test that request() encodes a list of numbers as a comma-separated string"""
        endpoint = 'search/tweets'
        url = self.get_url(endpoint)
        location = [37.781157, -122.39872, '1mi']
        self.register_response(responses.GET, url)

        self.api.request(endpoint, params={'geocode': location})

        self.assertEqual(url + '?geocode=37.781157%2C-122.39872%2C1mi', responses.calls[0].request.url)

    @responses.activate
    def test_request_should_ignore_bad_parameter(self):
        """Test that request() ignores unexpected parameter types"""
        endpoint = 'search/tweets'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url)

        self.api.request(endpoint, params={'geocode': self})

        self.assertEqual(url, responses.calls[0].request.url)

    @responses.activate
    def test_request_should_handle_file_as_parameter(self):
        """Test that request() pulls a file out of params for requests lib"""
        endpoint = 'account/update_profile_image'
        url = self.get_url(endpoint)
        self.register_response(responses.POST, url)

        mock_file = StringIO("Twython test image")
        self.api.request(endpoint, method='POST', params={'image': mock_file})

        self.assertIn(b'filename="image"', responses.calls[0].request.body)
        self.assertIn(b"Twython test image", responses.calls[0].request.body)

    @responses.activate
    def test_request_should_put_params_in_body_when_post(self):
        """Test that request() passes params as data when the request is a POST"""
        endpoint = 'statuses/update'
        url = self.get_url(endpoint)
        self.register_response(responses.POST, url)

        self.api.request(endpoint, method='POST', params={'status': 'this is a test'})

        self.assertIn(b'status=this+is+a+test', responses.calls[0].request.body)
        self.assertNotIn('status=this+is+a+test', responses.calls[0].request.url)

    @responses.activate
    def test_get_uses_get_method(self):
        """Test Twython generic GET request works"""
        endpoint = 'account/verify_credentials'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url)

        self.api.get(endpoint)

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(url, responses.calls[0].request.url)

    @responses.activate
    def test_post_uses_post_method(self):
        """Test Twython generic POST request works"""
        endpoint = 'statuses/update'
        url = self.get_url(endpoint)
        self.register_response(responses.POST, url)

        self.api.post(endpoint, params={'status': 'I love Twython!'})

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(url, responses.calls[0].request.url)

    def test_raise_twython_error_on_request_exception(self):
        """Test if TwythonError is raised by a RequestException"""
        with mock.patch.object(requests.Session, 'get') as get_mock:
            # mocking an ssl cert error
            get_mock.side_effect = requests.RequestException("hostname 'example.com' doesn't match ...")
            self.assertRaises(TwythonError, self.api.get, 'https://example.com')

    @responses.activate
    def test_request_should_get_convert_json_to_data(self):
        """Test that Twython converts JSON data to a Python object"""
        endpoint = 'statuses/show'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url, body='{"id": 210462857140252672}')

        data = self.api.request(endpoint, params={'id': 210462857140252672})

        self.assertEqual({'id': 210462857140252672}, data)

    @responses.activate
    def test_request_should_raise_exception_with_invalid_json(self):
        """Test that Twython handles invalid JSON (though Twitter should not return it)"""
        endpoint = 'statuses/show'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url, body='{"id: 210462857140252672}')

        self.assertRaises(TwythonError, self.api.request, endpoint, params={'id': 210462857140252672})

    @responses.activate
    def test_request_should_handle_401(self):
        """Test that Twython raises an auth error on 401 error"""
        endpoint = 'statuses/home_timeline'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url, body='{"errors":[{"message":"Error"}]}', status=401)

        self.assertRaises(TwythonAuthError, self.api.request, endpoint)

    @responses.activate
    def test_request_should_handle_400_for_missing_auth_data(self):
        """Test that Twython raises an auth error on 400 error when no oauth data sent"""
        endpoint = 'statuses/home_timeline'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url,
                               body='{"errors":[{"message":"Bad Authentication data"}]}', status=400)

        self.assertRaises(TwythonAuthError, self.api.request, endpoint)

    @responses.activate
    def test_request_should_handle_400_that_is_not_auth_related(self):
        """Test that Twython raises a normal error on 400 error when unrelated to authorization"""
        endpoint = 'statuses/home_timeline'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url,
                               body='{"errors":[{"message":"Bad request"}]}', status=400)

        self.assertRaises(TwythonError, self.api.request, endpoint)

    @responses.activate
    def test_request_should_handle_rate_limit(self):
        """Test that Twython raises an rate limit error on 429"""
        endpoint = 'statuses/home_timeline'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url,
                               body='{"errors":[{"message":"Rate Limit"}]}', status=429)

        self.assertRaises(TwythonRateLimitError, self.api.request, endpoint)

    @responses.activate
    def test_get_lastfunction_header_should_return_header(self):
        """Test getting last specific header of the last API call works"""
        endpoint = 'statuses/home_timeline'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url, adding_headers={'x-rate-limit-remaining': '37'})

        self.api.get(endpoint)

        value = self.api.get_lastfunction_header('x-rate-limit-remaining')
        self.assertEqual('37', value)
        value2 = self.api.get_lastfunction_header('does-not-exist')
        self.assertIsNone(value2)
        value3 = self.api.get_lastfunction_header('not-there-either', '96')
        self.assertEqual('96', value3)

    def test_get_lastfunction_header_should_raise_error_when_no_previous_call(self):
        """Test attempting to get a header when no API call was made raises a TwythonError"""
        self.assertRaises(TwythonError, self.api.get_lastfunction_header, 'no-api-call-was-made')

    @responses.activate
    def test_sends_correct_accept_encoding_header(self):
        """Test that Twython accepts compressed data."""
        endpoint = 'statuses/home_timeline'
        url = self.get_url(endpoint)
        self.register_response(responses.GET, url)

        self.api.get(endpoint)

        self.assertEqual(b'gzip, deflate', responses.calls[0].request.headers['Accept-Encoding'])

    # Static methods
    def test_construct_api_url(self):
        """Test constructing a Twitter API url works as we expect"""
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        constructed_url = self.api.construct_api_url(url, q='#twitter')
        self.assertEqual(constructed_url, 'https://api.twitter.com/1.1/search/tweets.json?q=%23twitter')

    def test_encode(self):
        """Test encoding UTF-8 works"""
        self.api.encode('Twython is awesome!')

    def test_html_for_tweet(self):
        """Test HTML for Tweet returns what we want"""
        tweet_text = self.api.html_for_tweet(test_tweet_object)
        self.assertEqual(test_tweet_html, tweet_text)

    def test_html_for_tweet_expanded_url(self):
        """Test using expanded url in HTML for Tweet displays full urls"""
        tweet_text = self.api.html_for_tweet(test_tweet_object,
                                             use_expanded_url=True)
        # Make sure full url is in HTML
        self.assertTrue('http://google.com' in tweet_text)

    def test_html_for_tweet_short_url(self):
        """Test using expanded url in HTML for Tweet displays full urls"""
        tweet_text = self.api.html_for_tweet(test_tweet_object, False)
        # Make sure HTML doesn't contain the display OR expanded url
        self.assertTrue('http://google.com' not in tweet_text)
        self.assertTrue('google.com' not in tweet_text)

    def test_html_for_tweet_symbols(self):
        tweet_text = self.api.html_for_tweet(test_tweet_symbols_object)
        # Should only link symbols listed in entities:
        self.assertTrue('<a href="https://twitter.com/search?q=%24AAPL" class="twython-symbol">$AAPL</a>' in tweet_text)
        self.assertTrue('<a href="https://twitter.com/search?q=%24ANOTHER" class="twython-symbol">$ANOTHER</a>' not in tweet_text)

    def test_html_for_tweet_compatmode(self):
        tweet_text = self.api.html_for_tweet(test_tweet_compat_object)
        # link to compat web status link
        self.assertTrue(
            u'<a href="https://t.co/SRmsuks2ru" class="twython-url">twitter.com/i/web/status/7…</a>' in tweet_text)

    def test_html_for_tweet_extendedmode(self):
        tweet_text = self.api.html_for_tweet(test_tweet_extended_object)
        # full tweet rendered with suffix
        self.assertEqual(test_tweet_extended_html, tweet_text)
