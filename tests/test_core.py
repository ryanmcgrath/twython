from twython import Twython, TwythonError, TwythonAuthError

from .config import (
    app_key, app_secret, oauth_token, oauth_token_secret,
    protected_twitter_1, protected_twitter_2, screen_name,
    test_tweet_id, test_list_slug, test_list_owner_screen_name,
    access_token, test_tweet_object, test_tweet_html
)

import time
import unittest
import responses


class TwythonAPITestCase(unittest.TestCase):
    def setUp(self):

        client_args = {
            'headers': {
                'User-Agent': '__twython__ Test'
            },
            'allow_redirects': False
        }

        oauth2_client_args = {
            'headers': {}  # This is so we can hit coverage that Twython sets User-Agent for us if none is supplied
        }

        self.api = Twython(app_key, app_secret,
                           oauth_token, oauth_token_secret,
                           client_args=client_args)

        self.oauth2_api = Twython(app_key, access_token=access_token,
                                  client_args=oauth2_client_args)

    @responses.activate
    def test_request_should_handle_full_endpoint(self):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        responses.add(responses.GET, url)

        self.api.request(url)

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(url, responses.calls[0].request.url)

    @responses.activate
    def test_request_should_handle_relative_endpoint(self):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        responses.add(responses.GET, url)

        self.api.request('search/tweets', version='1.1')

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(url, responses.calls[0].request.url)

    @responses.activate
    def test_request_should_post_request_regardless_of_case(self):
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        responses.add(responses.POST, url)

        self.api.request(url, method='POST')
        self.api.request(url, method='post')

        self.assertEqual(2, len(responses.calls))
        self.assertEqual(url, responses.calls[0].request.url)
        self.assertEqual(url, responses.calls[1].request.url)

    @responses.activate
    def test_request_should_throw_exception_with_invalid_http_method(self):
        #TODO(cash): should Twython catch the AttributeError and throw a TwythonError
        self.assertRaises(AttributeError, self.api.request, endpoint='search/tweets', method='INVALID')

    @responses.activate
    def test_request_should_encode_boolean_as_lowercase_string(self):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        responses.add(responses.GET, url)

        self.api.request('search/tweets', params={'include_entities': True})
        self.api.request('search/tweets', params={'include_entities': False})

        self.assertEqual(url + '?include_entities=true', responses.calls[0].request.url)
        self.assertEqual(url + '?include_entities=false', responses.calls[1].request.url)

    @responses.activate
    def test_request_should_handle_string_or_number_parameter(self):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        responses.add(responses.GET, url)

        self.api.request('search/tweets', params={'lang': 'es'})
        self.api.request('search/tweets', params={'count': 50})

        self.assertEqual(url + '?lang=es', responses.calls[0].request.url)
        self.assertEqual(url + '?count=50', responses.calls[1].request.url)

    @responses.activate
    def test_request_should_encode_string_list_as_string(self):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        location = ['37.781157', '-122.39872', '1mi']
        responses.add(responses.GET, url)

        self.api.request('search/tweets', params={'geocode': location})

        self.assertEqual(url + '?geocode=37.781157%2C-122.39872%2C1mi', responses.calls[0].request.url)

    @responses.activate
    def test_request_should_encode_number_list_as_string(self):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        location = [37.781157, -122.39872, '1mi']
        responses.add(responses.GET, url)

        self.api.request('search/tweets', params={'geocode': location})

        self.assertEqual(url + '?geocode=37.781157%2C-122.39872%2C1mi', responses.calls[0].request.url)

    @responses.activate
    def test_request_should_ignore_bad_parameter(self):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        responses.add(responses.GET, url)

        self.api.request('search/tweets', params={'geocode': self})

        self.assertEqual(url, responses.calls[0].request.url)

    def test_construct_api_url(self):
        """Test constructing a Twitter API url works as we expect"""
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        constructed_url = self.api.construct_api_url(url, q='#twitter')
        self.assertEqual(constructed_url, 'https://api.twitter.com/1.1/search/tweets.json?q=%23twitter')

    def test_get(self):
        """Test Twython generic GET request works"""
        self.api.get('account/verify_credentials')

    def test_post(self):
        """Test Twython generic POST request works, with a full url and
        with just an endpoint"""
        update_url = 'https://api.twitter.com/1.1/statuses/update.json'
        status = self.api.post(update_url, params={'status': 'I love Twython! %s' % int(time.time())})
        self.api.post('statuses/destroy/%s' % status['id_str'])

    def test_get_lastfunction_header(self):
        """Test getting last specific header of the last API call works"""
        self.api.get('statuses/home_timeline')
        self.api.get_lastfunction_header('x-rate-limit-remaining')

    def test_get_lastfunction_header_not_present(self):
        """Test getting specific header that does not exist from the last call returns None"""
        self.api.get('statuses/home_timeline')
        header = self.api.get_lastfunction_header('does-not-exist')
        self.assertEqual(header, None)

    def test_get_lastfunction_header_no_last_api_call(self):
        """Test attempting to get a header when no API call was made raises a TwythonError"""
        self.assertRaises(TwythonError, self.api.get_lastfunction_header,
                          'no-api-call-was-made')

    def test_cursor(self):
        """Test looping through the generator results works, at least once that is"""
        search = self.api.cursor(self.api.search, q='twitter', count=1)
        counter = 0
        while counter < 2:
            counter += 1
            result = next(search)
            new_id_str = int(result['id_str'])
            if counter == 1:
                prev_id_str = new_id_str
                time.sleep(1)  # Give time for another tweet to come into search
            if counter == 2:
                self.assertTrue(new_id_str > prev_id_str)

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
        # Make sure HTML doesn't contain the display OR exapanded url
        self.assertTrue(not 'http://google.com' in tweet_text)
        self.assertTrue(not 'google.com' in tweet_text)

    def test_raise_error_on_bad_ssl_cert(self):
        """Test TwythonError is raised by a RequestException when an actual HTTP happens"""
        self.assertRaises(TwythonError, self.api.get, 'https://example.com')
