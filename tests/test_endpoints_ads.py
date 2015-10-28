import base64
import datetime
import cStringIO
import urllib
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

    TEST_WEBSITE_CLICKS_LINE_ITEM = {
        'bid_type': 'MAX',
        'bid_amount_local_micro': 2000000,
        'product_type': 'PROMOTED_TWEETS',
        'placements': 'ALL_ON_TWITTER',
        'objective': 'WEBSITE_CLICKS',
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

    def test_get_available_platforms(self):
        available_platforms = self.api.get_available_platforms()
        self.assertTrue(len(available_platforms) > 0)

    def test_get_campaigns(self):
        campaigns = self.api.get_campaigns(test_account_id)
        self.assertTrue(len(campaigns) > 0)

    def test_create_and_delete_campaign(self):
        campaign_id = self._create_test_campaign()
        campaign_check = self.api.get_campaign(test_account_id, campaign_id)
        self.assertEqual(campaign_check['id'], campaign_id)
        self._delete_test_campaign(campaign_id)

    def _create_test_campaign(self):
        campaign = self.api.create_campaign(test_account_id, **self.TEST_CAMPAIGN)
        campaign_id = campaign['id']
        self.assertEqual(campaign['account_id'], test_account_id)
        self.assertIsNotNone(campaign_id)
        return campaign_id

    def _delete_test_campaign(self, campaign_id):
        is_deleted = self.api.delete_campaign(test_account_id, campaign_id)
        self.assertTrue(is_deleted)

    def test_create_line_item(self):
        campaign_id = self._create_test_campaign()
        response = self.api.create_line_item(test_account_id, campaign_id, **self.TEST_WEBSITE_CLICKS_LINE_ITEM)
        self.assertEqual(response['account_id'], test_account_id)
        self.assertEqual(response['campaign_id'], campaign_id)
        self._delete_test_campaign(campaign_id)

    def test_upload_image(self):
        response = self._upload_test_image()
        self.assertIsNotNone(response['media_id'])

    def _upload_test_image(self):
        image_file = urllib.urlopen('https://upload.wikimedia.org/wikipedia/commons/d/db/Patern_test.jpg').read()
        image_file_encoded = base64.b64encode(image_file)
        upload_data = {
            'media_data': image_file_encoded
            # the line below will have to be provided once we start uploading photos on behalf of advertisers
            # 'additional_owners': ''
        }
        response = self.api.upload_image(**upload_data)
        return response

    def test_create_cards_website(self):
        # campaign = self.api.create_campaign(test_account_id, **self.TEST_CAMPAIGN)
        # campaign_id = campaign['id']
        # self.assertEqual(campaign['account_id'], test_account_id)
        # line_item = self.api.create_line_item(test_account_id, campaign_id, **self.TEST_WEBSITE_CLICKS_LINE_ITEM)
        # self.assertEqual(line_item['account_id'], test_account_id)
        # self.assertEqual(line_item['campaign_id'], campaign_id)
        uploaded_image = self._upload_test_image()
        test_website_card = {
            'name': 'Zemanta Partnered with AdsNative for Programmatic Native Supply',
            'website_title': 'Zemanta Partnered with AdsNative for Programmatic Native Supply',
            'website_url': 'http://r1.zemanta.com/r/u1tllsoizjls/facebook/1009/92325/',
            'website_cta': 'READ_MORE',
            'image_media_id': uploaded_image['media_id_string']
        }
        response = self.api.create_website_card(test_account_id, **test_website_card)
        self.assertEqual(response['account_id'], test_account_id)
        # is_deleted = self.api.delete_campaign(test_account_id, campaign_id)
        # self.assertTrue(is_deleted)
