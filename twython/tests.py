#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json
import requests

import twythonrequests

class TestTwythonRequests(unittest.TestCase):
     def test_search(self):
         twitter = twythonrequests.Twython()
         result = twitter.search(q='python')
         self.assertTrue(result['results'])


if __name__ == "__main__":
    unittest.main()
