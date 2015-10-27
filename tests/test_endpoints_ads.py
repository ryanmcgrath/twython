import datetime
from twython import Twython, TwythonError, TwythonAuthError

from .config import (
    app_key, app_secret, oauth_token, oauth_token_secret,
    protected_twitter_1, protected_twitter_2, screen_name,
    test_tweet_id, test_list_slug, test_list_owner_screen_name,
    access_token, test_tweet_object, test_tweet_html, test_account_id, test_funding_instrument_id, unittest
)

import time
from twython.api_ads import TwythonAds


class TwythonEndpointsTestCase(unittest.TestCase):
    TEST_CAMPAIGN = {
        'name': 'Test Twitter campaign - Twython',
        'funding_instrument_id': test_funding_instrument_id,
        'start_time': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'daily_budget_amount_local_micro': 10 * 1000000,
        'paused': True
    }

    def setUp(self):

        client_args = {
            'headers': {
                'User-Agent': '__twython__ Test'
            },
            'allow_redirects': False
        }

        # This is so we can hit coverage that Twython sets
        # User-Agent for us if none is supplied
        oauth2_client_args = {
            'headers': {}
        }

        self.api = TwythonAds(app_key, app_secret,
                           oauth_token, oauth_token_secret,
                           client_args=client_args)

        self.oauth2_api = Twython(app_key, access_token=access_token,
                                  client_args=oauth2_client_args)

    def test_get_accounts(self):
        accounts = self.api.get_accounts()
        self.assertTrue(len(accounts) > 0)

    def test_get_account(self):
        account = self.api.get_account(test_account_id)
        self.assertEqual(account['id'], test_account_id)
        with self.assertRaises(TwythonError):
            self.api.get_account('1234')

    def test_get_account_features(self):
        account_features = self.api.get_account_features(test_account_id)
        self.assertTrue(len(account_features) > 0)

    def test_get_funding_instruments(self):
        funding_instruments = self.api.get_funding_instruments(test_account_id)
        self.assertTrue(len(funding_instruments) > 0)

    def test_get_funding_instrument(self):
        funding_instrument = self.api.get_funding_instrument(test_account_id, test_funding_instrument_id)
        self.assertEqual(funding_instrument['id'], test_funding_instrument_id)
        self.assertEqual(funding_instrument['account_id'], test_account_id)
        with self.assertRaises(TwythonError):
            self.api.get_funding_instrument('1234', '1234')

    def test_get_iab_categories(self):
        iab_categories = self.api.get_iab_categories()
        self.assertTrue(len(iab_categories) > 0)

    def test_get_campaigns(self):
        campaigns = self.api.get_campaigns(test_account_id)
        self.assertTrue(len(campaigns) > 0)

    def test_create_and_delete_campaign(self):
        campaign = self.api.create_campaign(test_account_id, **self.TEST_CAMPAIGN)
        campaign_id = campaign['id']
        self.assertEqual(campaign['account_id'], test_account_id)
        self.assertIsNotNone(campaign_id)
        campaign_check = self.api.get_campaign(test_account_id, campaign_id)
        self.assertEqual(campaign_check['id'], campaign_id)
        is_deleted = self.api.delete_campaign(test_account_id, campaign_id)
        self.assertTrue(is_deleted)

    def test_create_line_item(self):
        campaign = self.api.create_campaign(test_account_id, **self.TEST_CAMPAIGN)
        campaign_id = campaign['id']
        self.assertEqual(campaign['account_id'], test_account_id)
        website_clicks_line_item = {
            'bid_type': 'MAX',
            'bid_amount_local_micro': 2000000,
            'product_type': 'PROMOTED_TWEETS',
            'placements': 'ALL_ON_TWITTER',
            'objective': 'WEBSITE_CLICKS',
            'paused': True
        }
        response = self.api.create_line_item(test_account_id, campaign_id, **website_clicks_line_item)
        self.assertEqual(response['account_id'], test_account_id)
        self.assertEqual(response['campaign_id'], campaign_id)
        campaign_check = self.api.get_campaign(test_account_id, campaign_id)
        self.assertTrue(True)
