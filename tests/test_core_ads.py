from .config import (
    test_tweet_object, test_tweet_html, unittest
)

import responses
import requests
from twython.api_ads import TwythonAds

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
        self.api = TwythonAds('', '', '', '')