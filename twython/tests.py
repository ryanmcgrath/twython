#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json
import requests

import twythonrequests
twitter = twythonrequests.Twython()

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

if __name__ == "__main__":
    unittest.main()
