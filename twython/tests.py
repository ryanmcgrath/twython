#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json
import requests

import twython
twitter = twython.Twython()

class TestTwythonRequests(unittest.TestCase):
     def test_search(self):
         result = twitter.search(q='python')
         self.assertTrue(result['results'])

     def test_searchTwitter(self):
         result = twitter.searchTwitter(q='python')
         self.assertTrue(result['results'])

     def test_getProfileImageUrl(self):
         result = twitter.getProfileImageUrl(username='kracetheking')
         self.assertTrue(result)

     def test_shortenURL(self):
         result = twitter.shortenURL(url_to_shorten='http://google.com')
         self.assertEqual(result, 'http://is.gd/5JJNDX')


if __name__ == "__main__":
    unittest.main()
