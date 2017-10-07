# -*- coding: utf-8 -*-
from twython import Twython, TwythonError

from .config import (
    test_tweet_object, test_tweet_html, test_tweet_symbols_object,
    test_tweet_compat_object, test_tweet_extended_object,
    test_tweet_extended_html, test_tweet_identical_urls, test_tweet_reply,
    test_tweet_media,
    unittest
)


class TestHtmlForTweetTestCase(unittest.TestCase):
    def setUp(self):
        self.api = Twython('', '', '', '')

    def test_basic(self):
        """Test HTML for Tweet returns what we want"""
        tweet_text = self.api.html_for_tweet(test_tweet_object)
        self.assertEqual(test_tweet_html, tweet_text)

    def test_reply(self):
        """Test HTML for Tweet links the replied-to username."""
        tweet_text = self.api.html_for_tweet(test_tweet_reply)
        self.assertEqual(tweet_text,
                u'<span class="twython-tweet-prefix"><a href="https://twitter.com/philgyford" class="twython-mention">@philgyford</a> </span>Here’s a test tweet that goes on as much as possible and includes an image. Hi to my fans in testland!<span class="twython-tweet-suffix"> https://t.co/tzhyk2QWSr</span>')

    def test_expanded_url(self):
        """Test using expanded url in HTML for Tweet displays full urls"""
        tweet_text = self.api.html_for_tweet(test_tweet_object,
                                             use_expanded_url=True)
        # Make sure full url is in HTML
        self.assertTrue('http://google.com' in tweet_text)

    def test_short_url(self):
        """Test using expanded url in HTML for Tweet displays full urls"""
        tweet_text = self.api.html_for_tweet(test_tweet_object, False)
        # Make sure HTML doesn't contain the display OR expanded url
        self.assertTrue('http://google.com' not in tweet_text)
        self.assertTrue('google.com' not in tweet_text)

    def test_identical_urls(self):
        """If the 'url's for different url entities are identical, they should link correctly."""
        tweet_text = self.api.html_for_tweet(test_tweet_identical_urls)
        self.assertEqual(tweet_text,
                u'Use Cases, Trials and Making 5G a Reality <a href="https://t.co/W0uArTMk9N" class="twython-url">buff.ly/2sEhrgO</a> #5G #innovation via @5GWorldSeries <a href="https://t.co/W0uArTMk9N" class="twython-url">buff.ly/2sEhrgO</a>')

    def test_symbols(self):
        tweet_text = self.api.html_for_tweet(test_tweet_symbols_object)
        # Should only link symbols listed in entities:
        self.assertTrue('<a href="https://twitter.com/search?q=%24AAPL" class="twython-symbol">$AAPL</a>' in tweet_text)
        self.assertTrue('<a href="https://twitter.com/search?q=%24ANOTHER" class="twython-symbol">$ANOTHER</a>' not in tweet_text)

    def test_no_symbols(self):
        """Should still work if tweet object has no symbols list"""
        tweet = test_tweet_symbols_object
        # Save a copy:
        symbols = tweet['entities']['symbols']
        del tweet['entities']['symbols']
        tweet_text = self.api.html_for_tweet(tweet)
        self.assertTrue('symbols: $AAPL and' in tweet_text)
        self.assertTrue('and $ANOTHER and $A.' in tweet_text)
        # Put the symbols back:
        test_tweet_symbols_object['entities']['symbols'] = symbols

    def test_compatmode(self):
        tweet_text = self.api.html_for_tweet(test_tweet_compat_object)
        # link to compat web status link
        self.assertTrue(
            u'<a href="https://t.co/SRmsuks2ru" class="twython-url">twitter.com/i/web/status/7…</a>' in tweet_text)

    def test_extendedmode(self):
        tweet_text = self.api.html_for_tweet(test_tweet_extended_object)
        # full tweet rendered with suffix
        self.assertEqual(test_tweet_extended_html, tweet_text)

    def test_media(self):
        tweet_text = self.api.html_for_tweet(test_tweet_media)

        self.assertEqual(
            """I made some D3.js charts showing the years covered by books in a series compared to their publishing dates <a href="https://t.co/2yUmmn3TOc" class="twython-url">gyford.com/phil/writing/2…</a> <a href="https://t.co/OwNc6uJklg" class="twython-media">pic.twitter.com/OwNc6uJklg</a>""",
            tweet_text)

