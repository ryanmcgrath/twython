# -*- coding: utf-8 -*-
import json
import os

from twython import Twython, TwythonError

from .config import unittest


class TestHtmlForTweetTestCase(unittest.TestCase):
    def setUp(self):
        self.api = Twython('', '', '', '')

    def load_tweet(self, name):
        f = open(os.path.join(
                os.path.dirname(__file__),
                'tweets',
                '%s.json' % name
            ))
        tweet = json.load(f)
        f.close()
        return tweet

    def test_basic(self):
        """Test HTML for Tweet returns what we want"""
        tweet_object = self.load_tweet('basic')
        tweet_text = self.api.html_for_tweet(tweet_object)
        self.assertEqual(tweet_text,
            '<a href="http://t.co/FCmXyI6VHd" class="twython-url">google.com</a> is a <a href="https://twitter.com/search?q=%23cool" class="twython-hashtag">#cool</a> site, lol! <a href="https://twitter.com/mikehelmick" class="twython-mention">@mikehelmick</a> shd <a href="https://twitter.com/search?q=%23checkitout" class="twython-hashtag">#checkitout</a>. Love, <a href="https://twitter.com/__twython__" class="twython-mention">@__twython__</a> <a href="https://t.co/67pwRvY6z9" class="twython-url">github.com</a> <a href="http://t.co/N6InAO4B71" class="twython-media">pic.twitter.com/N6InAO4B71</a>')

    def test_reply(self):
        """Test HTML for Tweet links the replied-to username."""
        tweet_object = self.load_tweet('reply')
        tweet_text = self.api.html_for_tweet(tweet_object)
        self.assertEqual(tweet_text,
                u'<span class="twython-tweet-prefix"><a href="https://twitter.com/philgyford" class="twython-mention">@philgyford</a> </span>Here’s a test tweet that goes on as much as possible and includes an image. Hi to my fans in testland!<span class="twython-tweet-suffix"> https://t.co/tzhyk2QWSr</span>')

    def test_expanded_url(self):
        """Test using expanded url in HTML for Tweet displays full urls"""
        tweet_object = self.load_tweet('basic')
        tweet_text = self.api.html_for_tweet(tweet_object,
                                             use_expanded_url=True)
        # Make sure full url is in HTML
        self.assertTrue('http://google.com' in tweet_text)

    def test_short_url(self):
        """Test using expanded url in HTML for Tweet displays full urls"""
        tweet_object = self.load_tweet('basic')
        tweet_text = self.api.html_for_tweet(tweet_object, False)
        # Make sure HTML doesn't contain the display OR expanded url
        self.assertTrue('http://google.com' not in tweet_text)
        self.assertTrue('google.com' not in tweet_text)

    def test_identical_urls(self):
        """If the 'url's for different url entities are identical, they should link correctly."""
        tweet_object = self.load_tweet('identical_urls')
        tweet_text = self.api.html_for_tweet(tweet_object)
        self.assertEqual(tweet_text,
                u'Use Cases, Trials and Making 5G a Reality <a href="https://t.co/W0uArTMk9N" class="twython-url">buff.ly/2sEhrgO</a> #5G #innovation via @5GWorldSeries <a href="https://t.co/W0uArTMk9N" class="twython-url">buff.ly/2sEhrgO</a>')

    def test_symbols(self):
        tweet_object = self.load_tweet('symbols')
        tweet_text = self.api.html_for_tweet(tweet_object)
        # Should only link symbols listed in entities:
        self.assertTrue('<a href="https://twitter.com/search?q=%24AAPL" class="twython-symbol">$AAPL</a>' in tweet_text)
        self.assertTrue('<a href="https://twitter.com/search?q=%24ANOTHER" class="twython-symbol">$ANOTHER</a>' not in tweet_text)

    def test_no_symbols(self):
        """Should still work if tweet object has no symbols list"""
        tweet = self.load_tweet('symbols')
        # Save a copy:
        symbols = tweet['entities']['symbols']
        del tweet['entities']['symbols']
        tweet_text = self.api.html_for_tweet(tweet)
        self.assertTrue('symbols: $AAPL and' in tweet_text)
        self.assertTrue('and $ANOTHER and $A.' in tweet_text)

    def test_compatmode(self):
        tweet_object = self.load_tweet('compat')
        tweet_text = self.api.html_for_tweet(tweet_object)
        # link to compat web status link
        self.assertTrue(
            u'<a href="https://t.co/SRmsuks2ru" class="twython-url">twitter.com/i/web/status/7…</a>' in tweet_text)

    def test_extendedmode(self):
        tweet_object = self.load_tweet('extended')
        tweet_text = self.api.html_for_tweet(tweet_object)
        # full tweet rendered with suffix
        self.assertEqual(tweet_text,
            'Say more about what\'s happening! Rolling out now: photos, videos, GIFs, polls, and Quote Tweets no longer count toward your 140 characters.<span class="twython-tweet-suffix"> <a href="https://t.co/I9pUC0NdZC" class="twython-media">pic.twitter.com/I9pUC0NdZC</a></span>')

    def test_entities_with_prefix(self):
        """
        If there is a username mention at the start of a tweet it's in the
        "prefix" and so isn't part of the main tweet display text.
        But its length is still counted in the indices of any subsequent
        mentions, urls, hashtags, etc.
        """
        self.maxDiff = 2200
        tweet_object = self.load_tweet('entities_with_prefix')
        tweet_text = self.api.html_for_tweet(tweet_object)
        self.assertEqual(tweet_text,
            u'<span class="twython-tweet-prefix"><a href="https://twitter.com/philgyford" class="twython-mention">@philgyford</a> </span>This is a test for <a href="https://twitter.com/visionphil" class="twython-mention">@visionphil</a> that includes a link <a href="https://t.co/sKw4J3A8SZ" class="twython-url">example.org</a> and <a href="https://twitter.com/search?q=%23hashtag" class="twython-hashtag">#hashtag</a> and X for good measure AND that is longer than 140 characters. <a href="https://t.co/jnQdy7Zg7u" class="twython-url">example.com</a>')

    def test_media(self):
        tweet_object = self.load_tweet('media')
        tweet_text = self.api.html_for_tweet(tweet_object)

        self.assertEqual(
            u"""I made some D3.js charts showing the years covered by books in a series compared to their publishing dates <a href="https://t.co/2yUmmn3TOc" class="twython-url">gyford.com/phil/writing/2\u2026</a><span class="twython-tweet-suffix"> <a href="https://t.co/OwNc6uJklg" class="twython-media">pic.twitter.com/OwNc6uJklg</a></span>""",
            tweet_text)

    def test_quoted(self):
        "With expand_quoted_status=True it should include a quoted tweet."
        tweet_object = self.load_tweet('quoted')
        tweet_text = self.api.html_for_tweet(tweet_object,
                                             expand_quoted_status=True)
        self.assertEqual(
                u"""Here\u2019s a quoted tweet. <a href="https://t.co/3neKzof0gT" class="twython-url">twitter.com/philgyford/sta\u2026</a><blockquote class="twython-quote">The quoted tweet text.<cite><a href="https://twitter.com/philgyford/status/917699069916729344"><span class="twython-quote-user-name">Phil Gyford</span><span class="twython-quote-user-screenname">@philgyford</span></a></cite></blockquote>""",
                tweet_text)

    def test_retweet(self):
        "With expand_quoted_status=True it should include a quoted tweet."
        tweet_object = self.load_tweet('retweet')
        tweet_text = self.api.html_for_tweet(tweet_object)

        self.assertEqual(
                u"""My aunt and uncle in a very ill humour one with another, but I made shift with much ado to keep them from scolding.""",
                tweet_text)

