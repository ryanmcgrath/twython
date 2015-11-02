import base64
import datetime
import urllib

from twython import Twython, TwythonError
from .config import (
    app_key, app_secret, oauth_token, oauth_token_secret,
    access_token, test_account_id, test_funding_instrument_id, test_campaign_id, unittest
)
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

    @unittest.skip('skipping non-updated test')
    def test_get_accounts(self):
        accounts = self.api.get_accounts()
        self.assertTrue(len(accounts) >= 0)

    @unittest.skip('skipping non-updated test')
    def test_get_account(self):
        account = self.api.get_account(test_account_id)
        self.assertEqual(account['id'], test_account_id)
        with self.assertRaises(TwythonError):
            self.api.get_account('1234')

    @unittest.skip('skipping non-updated test')
    def test_get_account_features(self):
        account_features = self.api.get_account_features(test_account_id)
        self.assertTrue(len(account_features) >= 0)

    @unittest.skip('skipping non-updated test')
    def test_get_funding_instruments(self):
        funding_instruments = self.api.get_funding_instruments(test_account_id)
        self.assertTrue(len(funding_instruments) >= 0)

    @unittest.skip('skipping non-updated test')
    def test_get_funding_instrument(self):
        funding_instrument = self.api.get_funding_instrument(test_account_id, test_funding_instrument_id)
        self.assertEqual(funding_instrument['id'], test_funding_instrument_id)
        self.assertEqual(funding_instrument['account_id'], test_account_id)
        with self.assertRaises(TwythonError):
            self.api.get_funding_instrument('1234', '1234')

    @unittest.skip('skipping non-updated test')
    def test_get_iab_categories(self):
        iab_categories = self.api.get_iab_categories()
        self.assertTrue(len(iab_categories) >= 0)

    @unittest.skip('skipping non-updated test')
    def test_get_available_platforms(self):
        available_platforms = self.api.get_available_platforms()
        self.assertTrue(len(available_platforms) >= 0)

    @unittest.skip('skipping non-updated test')
    def test_get_available_locations(self):
        params = {
            'location_type': 'CITY',
            'country_code': 'US'
        }
        available_locations = self.api.get_available_locations(**params)
        self.assertTrue(len(available_locations) > 0)

    @unittest.skip('skipping non-updated test')
    def test_get_campaigns(self):
        campaigns = self.api.get_campaigns(test_account_id)
        self.assertTrue(len(campaigns) >= 0)

    @unittest.skip('skipping non-updated test')
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

    @unittest.skip('skipping non-updated test')
    def test_create_and_delete_line_item(self):
        campaign_id = self._create_test_campaign()
        line_item_id = self._create_test_line_item(campaign_id)
        line_items = self.api.get_line_items(test_account_id, campaign_id)
        self.assertTrue(len(line_items) > 0)
        self._delete_test_line_item(line_item_id)
        self._delete_test_campaign(campaign_id)

    def _create_test_line_item(self, campaign_id):
        response = self.api.create_line_item(test_account_id, campaign_id, **self.TEST_WEBSITE_CLICKS_LINE_ITEM)
        line_item_id = response['id']
        self.assertEqual(response['account_id'], test_account_id)
        self.assertEqual(response['campaign_id'], campaign_id)
        self.assertIsNotNone(line_item_id)
        return line_item_id

    def _delete_test_line_item(self, line_item_id):
        is_deleted = self.api.delete_line_item(test_account_id, line_item_id)
        self.assertTrue(is_deleted)

    @unittest.skip('skipping non-updated test')
    def test_upload_image(self):
        response = self._upload_test_image()
        self.assertIsNotNone(response['media_id'])

    def _upload_test_image(self):
        image_file = urllib.urlopen('https://openclipart.org/image/800px/svg_to_png/190042/1389527622.png').read()
        image_file_encoded = base64.b64encode(image_file)
        upload_data = {
            'media_data': image_file_encoded
            # the line below will have to be provided once we start uploading photos on behalf of advertisers
            # 'additional_owners': ''
        }
        response = self.api.upload_image(**upload_data)
        return response

    @unittest.skip('skipping non-updated test')
    def test_get_website_cards(self):
        response = self.api.get_website_cards(test_account_id)
        self.assertTrue(len(response) >= 0)

    @unittest.skip('skipping non-updated test')
    def test_create_and_delete_website_card(self):
        card_id = self._create_test_website_card()
        card = self.api.get_website_card(test_account_id, card_id)
        self.assertEqual(card['id'], card_id)
        self._delete_test_website_card(card_id)

    def _create_test_website_card(self):
        uploaded_image = self._upload_test_image()
        test_website_card = {
            'name': 'Zemanta Partnered with AdsNative for Programmatic Native Supply',
            'website_title': 'Zemanta Partnered with AdsNative for Programmatic Native Supply',
            'website_url': 'http://r1.zemanta.com/r/u1tllsoizjls/facebook/1009/92325/',
            'website_cta': 'READ_MORE',
            'image_media_id': uploaded_image['media_id_string']
        }
        response_create = self.api.create_website_card(test_account_id, **test_website_card)
        card_id = response_create['id']
        self.assertEqual(response_create['account_id'], test_account_id)
        self.assertIsNotNone(card_id)
        return card_id

    def _delete_test_website_card(self, card_id):
        response_delete = self.api.delete_website_card(test_account_id, card_id)
        self.assertEqual(response_delete['id'], card_id)

    @unittest.skip('skipping non-updated test')
    def test_create_promoted_only_tweet(self):
        card_id, tweet_id = self._create_test_promoted_only_tweet()
        self._delete_test_website_card(card_id)

    def _create_test_promoted_only_tweet(self):
        card_id = self._create_test_website_card()
        card = self.api.get_website_card(test_account_id, card_id)
        test_promoted_only_tweet = {
            'status': 'This is test tweet for website card: %s' % card['preview_url'],
            # 'as_user_id': '',
        }
        response = self.api.create_promoted_only_tweet(test_account_id, **test_promoted_only_tweet)
        tweet_id = response['id']
        self.assertIsNotNone(tweet_id)
        return card_id, tweet_id

    @unittest.skip('skipping non-updated test')
    def test_promote_and_unpromote_tweet(self):
        campaign_id = self._create_test_campaign()
        line_item_id = self._create_test_line_item(campaign_id)
        card_id, tweet_id = self._create_test_promoted_only_tweet()
        test_tweet_promotion = {
            'line_item_id': line_item_id,
            'tweet_ids': [tweet_id]
        }
        result_promote = self.api.promote_tweet(test_account_id, **test_tweet_promotion)
        self.assertTrue(len(result_promote) > 0)
        self.assertEqual(int(result_promote[0]['tweet_id']), tweet_id)
        promotion_id = result_promote[0]['id']
        self.assertIsNotNone(promotion_id)
        promoted_tweets = self.api.get_promoted_tweets(test_account_id, line_item_id)
        self.assertTrue(len(promoted_tweets) == 1)
        result_unpromotion = self.api.unpromote_tweet(test_account_id, promotion_id)
        self.assertTrue(result_unpromotion['deleted'])
        self.assertEqual(result_unpromotion['id'], promotion_id)
        self._delete_test_campaign(campaign_id)
        self._delete_test_website_card(card_id)

    @unittest.skip('skipping non-updated test')
    def test_add_targeting_criteria(self):
        campaign_id = self._create_test_campaign()
        line_item_id = self._create_test_line_item(campaign_id)
        criteria_ios_id = self._create_test_targeting_criteria(line_item_id, 'PLATFORM', '0')
        criteria_android_id = self._create_test_targeting_criteria(line_item_id, 'PLATFORM', '1')
        criteria_desktop_id = self._create_test_targeting_criteria(line_item_id, 'PLATFORM', '4')
        criteria_new_york_id = self._create_test_targeting_criteria(line_item_id, 'LOCATION', 'b6c2e04f1673337f')
        # since all the targeting criteria share the same id, we only have to do the removal once.
        self.api.remove_targeting_criteria(test_account_id, criteria_ios_id)
        self.api.remove_targeting_criteria(test_account_id, criteria_android_id)
        self.api.remove_targeting_criteria(test_account_id, criteria_desktop_id)
        self.api.remove_targeting_criteria(test_account_id, criteria_new_york_id)
        self._delete_test_line_item(line_item_id)
        self._delete_test_campaign(campaign_id)

    def _create_test_targeting_criteria(self, line_item_id, targeting_type, targeting_value):
        test_targeting_criteria_ios = {
            'targeting_type': targeting_type,
            'targeting_value': targeting_value
        }
        response_add = self.api.add_targeting_criteria(test_account_id, line_item_id, **test_targeting_criteria_ios)
        self.assertEqual(response_add['account_id'], test_account_id)
        self.assertEquals(response_add['line_item_id'], line_item_id)
        return response_add['id']

    @unittest.skip('skipping non-updated test')
    def test_get_stats_promoted_tweets(self):
        line_items = self.api.get_line_items(test_account_id, test_campaign_id)
        promoted_tweets = self.api.get_promoted_tweets(test_account_id, line_items[0]['id'])
        promoted_ids = [tweet['id'] for tweet in promoted_tweets]
        stats_query = {
            'start_time': '2015-10-29T00:00:00Z',
            'end_time': '2015-10-29T23:59:59Z',
            'granularity': 'TOTAL'
        }
        stats = self.api.get_stats_promoted_tweets(test_account_id, promoted_ids, **stats_query)
        self.assertTrue(len(stats) >= 0)
