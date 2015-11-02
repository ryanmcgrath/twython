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
        response = self.get('targeting_criteria/platforms', params=params)
        return response['data']

    def get_available_locations(self, **params):
        response = self.get('targeting_criteria/locations', params=params)
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

    def delete_line_item(self, account_id, line_item_id):
        response = self.delete('accounts/%s/line_items/%s' % (account_id, line_item_id))
        return response['data']['deleted']

    def get_line_items(self, account_id, campaign_id=None, **params):
        params_extended = params.copy()
        if campaign_id is not None:
            params_extended['campaign_ids'] = campaign_id
        response = self.get('accounts/%s/line_items' % account_id, params=params_extended)
        return response['data']

    def get_website_cards(self, account_id, **params):
        response = self.get('accounts/%s/cards/website' % account_id, params=params)
        return response['data']

    def get_website_card(self, account_id, card_id, **params):
        response = self.get('accounts/%s/cards/website/%s' % (account_id, card_id), params=params)
        return response['data']

    def create_website_card(self, account_id, **params):
        # TODO: handle the case where name, website_title, website_url are too long!
        response = self.post('accounts/%s/cards/website' % account_id, params=params)
        return response['data']

    def delete_website_card(self, account_id, card_id, **params):
        response = self.delete('accounts/%s/cards/website/%s' % (account_id, card_id), params=params)
        return response['data']

    def upload_image(self, **params):
        response = self.post('https://upload.twitter.com/1.1/media/upload.json', params=params)
        return response

    def create_promoted_only_tweet(self, account_id, **params):
        response = self.post('accounts/%s/tweet' % account_id, params=params)
        return response['data']

    def promote_tweet(self, account_id, **params):
        response = self.post('accounts/%s/promoted_tweets' % account_id, params=params)
        return response['data']

    def unpromote_tweet(self, account_id, promotion_id):
        response = self.delete('accounts/%s/promoted_tweets/%s' % (account_id, promotion_id))
        return response['data']

    def get_promoted_tweets(self, account_id, line_item_id=None, **params):
        params_extended = params.copy()
        if line_item_id is not None:
            params_extended['line_item_id'] = line_item_id
        response = self.get('accounts/%s/promoted_tweets' % account_id, params=params_extended)
        return response['data']

    def add_targeting_criteria(self, account_id, line_item_id, **params):
        params_extended = params.copy()
        params_extended['line_item_id'] = line_item_id
        response = self.post('accounts/%s/targeting_criteria' % account_id, params=params_extended)
        return response['data']

    def remove_targeting_criteria(self, account_id, criteria_id):
        response = self.delete('accounts/%s/targeting_criteria/%s' % (account_id, criteria_id))
        return response['data']

    def get_stats_promoted_tweets(self, account_id, promoted_tweet_ids, **params):
        # the promoted_tweet_ids contains a list of up to 20 identifiers:
        # https://dev.twitter.com/ads/reference/get/stats/accounts/%3Aaccount_id/promoted_tweets
        stats = []
        max_chunk_size = 20
        for i in range(0, len(promoted_tweet_ids), max_chunk_size):
            chunk = promoted_tweet_ids[i:i + max_chunk_size]
            params_extended = params.copy()
            params_extended['promoted_tweet_ids'] = ",".join(chunk)
            response = self.get('stats/accounts/%s/promoted_tweets' % account_id, params=params_extended)
            stats.extend(response['data'])
        return stats
