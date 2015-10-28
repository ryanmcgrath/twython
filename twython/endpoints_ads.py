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

    def get_account_features(self, account_id, **params):
        response = self.get('accounts/%s/features' % account_id, params=params)
        return response['data']

    def get_funding_instruments(self, account_id, **params):
        response = self.get('accounts/%s/funding_instruments' % account_id, params=params)
        return response['data']

    def get_funding_instrument(self, account_id, funding_instrument_id, **params):
        response = self.get('accounts/%s/funding_instruments/%s' % (account_id, funding_instrument_id), params=params)
        return response['data']

    def get_iab_categories(self, **params):
        response = self.get('iab_categories', params=params)
        return response['data']

    def get_available_platforms(self, **params):
        response = self.get('targeting_criteria/platforms')
        return response['data']

    def get_campaigns(self, account_id, **params):
        response = self.get('accounts/%s/campaigns' % account_id, params=params)
        return response['data']

    def get_campaign(self, account_id, campaign_id, **params):
        response = self.get('accounts/%s/campaigns/%s' % (account_id, campaign_id), params=params)
        return response['data']

    def create_campaign(self, account_id, **params):
        response = self.post('accounts/%s/campaigns' % account_id, params=params)
        return response['data']

    def delete_campaign(self, account_id, campaign_id):
        response = self.delete('accounts/%s/campaigns/%s' % (account_id, campaign_id))
        return response['data']['deleted']

    def create_line_item(self, account_id, campaign_id, **params):
        params_extended = params.copy()
        params_extended['campaign_id'] = campaign_id
        response = self.post('accounts/%s/line_items' % account_id, params=params_extended)
        return response['data']

    def create_website_card(self, account_id, **params):
        # TODO: handle the case where name, website_title, website_url are too long!
        response = self.post('accounts/%s/cards/website' % account_id, params=params)
        return response['data']

    def upload_image(self, **params):
        response = self.post('https://upload.twitter.com/1.1/media/upload.json', params=params)
        return response
