# -*- coding: utf-8 -*-

"""
twython.endpoints_ads
~~~~~~~~~~~~~~~~~

This module adds Twitter Ads API support to the Twython library.
This module provides a mixin for a :class:`TwythonAds <TwythonAds>` instance.
Parameters that need to be embedded in the API url just need to be passed
as a keyword argument.

e.g. TwythonAds.retweet(id=12345)

The API functions that are implemented in this module are documented at:
https://dev.twitter.com/ads/overview
"""

import os
import warnings
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class EndpointsAdsMixin(object):
    def get_accounts(self, **params):
        response = self.get('accounts', params=params)
        return response['data']

    def get_account(self, account_id, **params):
        response = self.get('accounts/%s' % account_id, params=params)
        return response['data']

    def get_funding_instruments(self, account_id, **params):
        response = self.get('accounts/%s/funding_instruments' % account_id, params=params)
        return response['data']

    def get_funding_instrument(self, account_id, funding_instrument_id, **params):
        response = self.get('accounts/%s/funding_instruments/%s' % (account_id, funding_instrument_id), params=params)
        return response['data']

    def get_campaigns(self, account_id, **params):
        response = self.get('accounts/%s/campaigns' % account_id, params)
        return response['data']

    def create_campaign(self, account_id, **params):
        response = self.post('accounts/%s/campaigns' % account_id, params)
        return response['data']
