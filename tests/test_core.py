from twython import Twython, TwythonError, TwythonAuthError

from .config import (
    app_key, app_secret, oauth_token, oauth_token_secret,
    protected_twitter_1, protected_twitter_2, screen_name,
    test_tweet_id, test_list_slug, test_list_owner_screen_name,
    access_token, test_tweet_object, test_tweet_html
)

import time
import unittest


class TwythonAPITestCase(unittest.TestCase):
    def setUp(self):

        client_args = {
            'headers': {
                'User-Agent': '__twython__ Test'
            },
            'allow_redirects': False
        }

        oauth2_client_args = {
            'headers': {}  # This is so we can hit coverage that Twython sets User-Agent for us if none is supplied
        }

        self.api = Twython(app_key, app_secret,
                           oauth_token, oauth_token_secret,
                           client_args=client_args)

        self.oauth2_api = Twython(app_key, access_token=access_token,
                                  client_args=oauth2_client_args)

    def test_construct_api_url(self):
        """Test constructing a Twitter API url works as we expect"""
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        constructed_url = self.api.construct_api_url(url, q='#twitter')
        self.assertEqual(constructed_url, 'https://api.twitter.com/1.1/search/tweets.json?q=%23twitter')

    def test_get(self):
        """Test Twython generic GET request works"""
        self.api.get('account/verify_credentials')

    def test_post(self):
        """Test Twython generic POST request works, with a full url and
        with just an endpoint"""
        update_url = 'https://api.twitter.com/1.1/statuses/update.json'
        status = self.api.post(update_url, params={'status': 'I love Twython! %s' % int(time.time())})
        self.api.post('statuses/destroy/%s' % status['id_str'])

    def test_get_lastfunction_header(self):
        """Test getting last specific header of the last API call works"""
        self.api.get('statuses/home_timeline')
        self.api.get_lastfunction_header('x-rate-limit-remaining')

    def test_get_lastfunction_header_not_present(self):
        """Test getting specific header that does not exist from the last call returns None"""
        self.api.get('statuses/home_timeline')
        header = self.api.get_lastfunction_header('does-not-exist')
        self.assertEqual(header, None)

    def test_get_lastfunction_header_no_last_api_call(self):
        """Test attempting to get a header when no API call was made raises a TwythonError"""
        self.assertRaises(TwythonError, self.api.get_lastfunction_header,
                          'no-api-call-was-made')

    def test_cursor(self):
        """Test looping through the generator results works, at least once that is"""
        search = self.api.cursor(self.api.search, q='twitter', count=1)
        counter = 0
        while counter < 2:
            counter += 1
            result = next(search)
            new_id_str = int(result['id_str'])
            if counter == 1:
                prev_id_str = new_id_str
                time.sleep(1)  # Give time for another tweet to come into search
            if counter == 2:
                self.assertTrue(new_id_str > prev_id_str)

    def test_encode(self):
        """Test encoding UTF-8 works"""
        self.api.encode('Twython is awesome!')

    def test_html_for_tweet(self):
        """Test HTML for Tweet returns what we want"""
        tweet_text = self.api.html_for_tweet(test_tweet_object)
        self.assertEqual(test_tweet_html, tweet_text)

    def test_html_for_tweet_expanded_url(self):
        """Test using expanded url in HTML for Tweet displays full urls"""
        tweet_text = self.api.html_for_tweet(test_tweet_object,
                                             use_expanded_url=True)
        # Make sure full url is in HTML
        self.assertTrue('http://google.com' in tweet_text)

    def test_html_for_tweet_short_url(self):
        """Test using expanded url in HTML for Tweet displays full urls"""
        tweet_text = self.api.html_for_tweet(test_tweet_object, False)
        # Make sure HTML doesn't contain the display OR exapanded url
        self.assertTrue(not 'http://google.com' in tweet_text)
        self.assertTrue(not 'google.com' in tweet_text)

    def test_raise_error_on_bad_ssl_cert(self):
        """Test TwythonError is raised by a RequestException when an actual HTTP happens"""
        self.assertRaises(TwythonError, self.api.get, 'https://example.com')

    # Timelines
    def test_get_mentions_timeline(self):
        """Test returning mentions timeline for authenticated user succeeds"""
        self.api.get_mentions_timeline()

    def test_get_user_timeline(self):
        """Test returning timeline for authenticated user and random user
        succeeds"""
        self.api.get_user_timeline()  # Authenticated User Timeline
        self.api.get_user_timeline(screen_name='twitter')  # Random User Timeline

    def test_get_protected_user_timeline_following(self):
        """Test returning a protected user timeline who you are following
        succeeds"""
        self.api.get_user_timeline(screen_name=protected_twitter_1)

    def test_get_protected_user_timeline_not_following(self):
        """Test returning a protected user timeline who you are not following
        fails and raise a TwythonAuthError"""
        self.assertRaises(TwythonAuthError, self.api.get_user_timeline,
                          screen_name=protected_twitter_2)

    def test_retweeted_of_me(self):
        """Test that getting recent tweets by authenticated user that have
        been retweeted by others succeeds"""
        self.api.retweeted_of_me()

    def test_get_home_timeline(self):
        """Test returning home timeline for authenticated user succeeds"""
        self.api.get_home_timeline()

    # Tweets
    def test_get_retweets(self):
        """Test getting retweets of a specific tweet succeeds"""
        self.api.get_retweets(id=test_tweet_id)

    def test_show_status(self):
        """Test returning a single status details succeeds"""
        self.api.show_status(id=test_tweet_id)

    def test_update_and_destroy_status(self):
        """Test updating and deleting a status succeeds"""
        status = self.api.update_status(status='Test post just to get deleted :( %s' % int(time.time()))
        self.api.destroy_status(id=status['id_str'])

    def test_get_oembed_tweet(self):
        """Test getting info to embed tweet on Third Party site succeeds"""
        self.api.get_oembed_tweet(id='99530515043983360')

    def test_get_retweeters_ids(self):
        """Test getting ids for people who retweeted a tweet succeeds"""
        self.api.get_retweeters_ids(id='99530515043983360')

    # Search
    def test_search(self):
        """Test searching tweets succeeds"""
        self.api.search(q='twitter')

    # Direct Messages
    def test_get_direct_messages(self):
        """Test getting the authenticated users direct messages succeeds"""
        self.api.get_direct_messages()

    def test_get_sent_messages(self):
        """Test getting the authenticated users direct messages they've
        sent succeeds"""
        self.api.get_sent_messages()

    def test_send_get_and_destroy_direct_message(self):
        """Test sending, getting, then destory a direct message succeeds"""
        message = self.api.send_direct_message(screen_name=protected_twitter_1,
                                               text='Hey d00d! %s' % int(time.time()))

        self.api.get_direct_message(id=message['id_str'])
        self.api.destroy_direct_message(id=message['id_str'])

    def test_send_direct_message_to_non_follower(self):
        """Test sending a direct message to someone who doesn't follow you
        fails"""
        self.assertRaises(TwythonError, self.api.send_direct_message,
                          screen_name=protected_twitter_2, text='Yo, man! %s' % int(time.time()))

    # Friends & Followers
    def test_get_user_ids_of_blocked_retweets(self):
        """Test that collection of user_ids that the authenticated user does
        not want to receive retweets from succeeds"""
        self.api.get_user_ids_of_blocked_retweets(stringify_ids=True)

    def test_get_friends_ids(self):
        """Test returning ids of users the authenticated user and then a random
        user is following succeeds"""
        self.api.get_friends_ids()
        self.api.get_friends_ids(screen_name='twitter')

    def test_get_followers_ids(self):
        """Test returning ids of users the authenticated user and then a random
        user are followed by succeeds"""
        self.api.get_followers_ids()
        self.api.get_followers_ids(screen_name='twitter')

    def test_lookup_friendships(self):
        """Test returning relationships of the authenticating user to the
        comma-separated list of up to 100 screen_names or user_ids provided
        succeeds"""
        self.api.lookup_friendships(screen_name='twitter,ryanmcgrath')

    def test_get_incoming_friendship_ids(self):
        """Test returning incoming friendship ids succeeds"""
        self.api.get_incoming_friendship_ids()

    def test_get_outgoing_friendship_ids(self):
        """Test returning outgoing friendship ids succeeds"""
        self.api.get_outgoing_friendship_ids()

    def test_create_friendship(self):
        """Test creating a friendship succeeds"""
        self.api.create_friendship(screen_name='justinbieber')

    def test_destroy_friendship(self):
        """Test destroying a friendship succeeds"""
        self.api.destroy_friendship(screen_name='justinbieber')

    def test_update_friendship(self):
        """Test updating friendships succeeds"""
        self.api.update_friendship(screen_name=protected_twitter_1,
                                   retweets='true')

        self.api.update_friendship(screen_name=protected_twitter_1,
                                   retweets=False)

    def test_show_friendships(self):
        """Test showing specific friendship succeeds"""
        self.api.show_friendship(target_screen_name=protected_twitter_1)

    def test_get_friends_list(self):
        """Test getting list of users authenticated user then random user is
        following succeeds"""
        self.api.get_friends_list()
        self.api.get_friends_list(screen_name='twitter')

    def test_get_followers_list(self):
        """Test getting list of users authenticated user then random user are
        followed by succeeds"""
        self.api.get_followers_list()
        self.api.get_followers_list(screen_name='twitter')

    # Users
    def test_get_account_settings(self):
        """Test getting the authenticated user account settings succeeds"""
        self.api.get_account_settings()

    def test_verify_credentials(self):
        """Test representation of the authenticated user call succeeds"""
        self.api.verify_credentials()

    def test_update_account_settings(self):
        """Test updating a user account settings succeeds"""
        self.api.update_account_settings(lang='en')

    def test_update_delivery_service(self):
        """Test updating delivery settings fails because we don't have
        a mobile number on the account"""
        self.assertRaises(TwythonError, self.api.update_delivery_service,
                          device='none')

    def test_update_profile(self):
        """Test updating profile succeeds"""
        self.api.update_profile(include_entities='true')

    def test_update_profile_colors(self):
        """Test updating profile colors succeeds"""
        self.api.update_profile_colors(profile_background_color='3D3D3D')

    def test_list_blocks(self):
        """Test listing users who are blocked by the authenticated user
        succeeds"""
        self.api.list_blocks()

    def test_list_block_ids(self):
        """Test listing user ids who are blocked by the authenticated user
        succeeds"""
        self.api.list_block_ids()

    def test_create_block(self):
        """Test blocking a user succeeds"""
        self.api.create_block(screen_name='justinbieber')

    def test_destroy_block(self):
        """Test unblocking a user succeeds"""
        self.api.destroy_block(screen_name='justinbieber')

    def test_lookup_user(self):
        """Test listing a number of user objects succeeds"""
        self.api.lookup_user(screen_name='twitter,justinbieber')

    def test_show_user(self):
        """Test showing one user works"""
        self.api.show_user(screen_name='twitter')

    def test_search_users(self):
        """Test that searching for users succeeds"""
        self.api.search_users(q='Twitter API')

    def test_get_contributees(self):
        """Test returning list of accounts the specified user can
        contribute to succeeds"""
        self.api.get_contributees(screen_name='TechCrunch')

    def test_get_contributors(self):
        """Test returning list of accounts that contribute to the
        authenticated user fails because we are not a Contributor account"""
        self.assertRaises(TwythonError, self.api.get_contributors,
                          screen_name=screen_name)

    def test_remove_profile_banner(self):
        """Test removing profile banner succeeds"""
        self.api.remove_profile_banner()

    def test_get_profile_banner_sizes(self):
        """Test getting list of profile banner sizes fails because
        we have not uploaded a profile banner"""
        self.assertRaises(TwythonError, self.api.get_profile_banner_sizes)

    # Suggested Users
    def test_get_user_suggestions_by_slug(self):
        """Test getting user suggestions by slug succeeds"""
        self.api.get_user_suggestions_by_slug(slug='twitter')

    def test_get_user_suggestions(self):
        """Test getting user suggestions succeeds"""
        self.api.get_user_suggestions()

    def test_get_user_suggestions_statuses_by_slug(self):
        """Test getting status of suggested users succeeds"""
        self.api.get_user_suggestions_statuses_by_slug(slug='funny')

    # Favorites
    def test_get_favorites(self):
        """Test getting list of favorites for the authenticated
        user succeeds"""
        self.api.get_favorites()

    def test_create_and_destroy_favorite(self):
        """Test creating and destroying a favorite on a tweet succeeds"""
        self.api.create_favorite(id=test_tweet_id)
        self.api.destroy_favorite(id=test_tweet_id)

    # Lists
    def test_show_lists(self):
        """Test show lists for specified user"""
        self.api.show_lists(screen_name='twitter')

    def test_get_list_statuses(self):
        """Test timeline of tweets authored by members of the
        specified list succeeds"""
        self.api.get_list_statuses(slug=test_list_slug,
                                   owner_screen_name=test_list_owner_screen_name)

    def test_create_update_destroy_list_add_remove_list_members(self):
        """Test create a list, adding and removing members then
        deleting the list succeeds"""
        the_list = self.api.create_list(name='Stuff %s' % int(time.time()))
        list_id = the_list['id_str']

        self.api.update_list(list_id=list_id, name='Stuff Renamed %s' % int(time.time()))

        screen_names = ['johncena', 'xbox']
        # Multi add/delete members
        self.api.create_list_members(list_id=list_id,
                                     screen_name=screen_names)
        self.api.delete_list_members(list_id=list_id,
                                     screen_name=screen_names)

        # Single add/delete member
        self.api.add_list_member(list_id=list_id, screen_name='justinbieber')
        self.api.delete_list_member(list_id=list_id, screen_name='justinbieber')

        self.api.delete_list(list_id=list_id)

    def test_get_list_subscribers(self):
        """Test list of subscribers of a specific list succeeds"""
        self.api.get_list_subscribers(slug=test_list_slug,
                                      owner_screen_name=test_list_owner_screen_name)

    def test_subscribe_is_subbed_and_unsubscribe_to_list(self):
        """Test subscribing, is a list sub and unsubbing to list succeeds"""
        self.api.subscribe_to_list(slug=test_list_slug,
                                   owner_screen_name=test_list_owner_screen_name)
        # Returns 404 if user is not a subscriber
        self.api.is_list_subscriber(slug=test_list_slug,
                                    owner_screen_name=test_list_owner_screen_name,
                                    screen_name=screen_name)
        self.api.unsubscribe_from_list(slug=test_list_slug,
                                       owner_screen_name=test_list_owner_screen_name)

    def test_is_list_member(self):
        """Test returning if specified user is member of a list succeeds"""
        # Returns 404 if not list member
        self.api.is_list_member(slug=test_list_slug,
                                owner_screen_name=test_list_owner_screen_name,
                                screen_name='themattharris')

    def test_get_list_members(self):
        """Test listing members of the specified list succeeds"""
        self.api.get_list_members(slug=test_list_slug,
                                  owner_screen_name=test_list_owner_screen_name)

    def test_get_specific_list(self):
        """Test getting specific list succeeds"""
        self.api.get_specific_list(slug=test_list_slug,
                                   owner_screen_name=test_list_owner_screen_name)

    def test_get_list_subscriptions(self):
        """Test collection of the lists the specified user is
        subscribed to succeeds"""
        self.api.get_list_subscriptions(screen_name='twitter')

    def test_show_owned_lists(self):
        """Test collection of lists the specified user owns succeeds"""
        self.api.show_owned_lists(screen_name='twitter')

    # Saved Searches
    def test_get_saved_searches(self):
        """Test getting list of saved searches for authenticated
        user succeeds"""
        self.api.get_saved_searches()

    def test_create_get_destroy_saved_search(self):
        """Test getting list of saved searches for authenticated
        user succeeds"""
        saved_search = self.api.create_saved_search(query='#Twitter')
        saved_search_id = saved_search['id_str']

        self.api.show_saved_search(id=saved_search_id)
        self.api.destroy_saved_search(id=saved_search_id)

    # Places & Geo
    def test_get_geo_info(self):
        """Test getting info about a geo location succeeds"""
        self.api.get_geo_info(place_id='df51dec6f4ee2b2c')

    def test_reverse_geo_code(self):
        """Test reversing geocode succeeds"""
        self.api.reverse_geocode(lat='37.76893497', long='-122.42284884')

    def test_search_geo(self):
        """Test search for places that can be attached
        to a statuses/update succeeds"""
        self.api.search_geo(query='Toronto')

    def test_get_similar_places(self):
        """Test locates places near the given coordinates which
        are similar in name succeeds"""
        self.api.get_similar_places(lat='37', long='-122', name='Twitter HQ')

    # Trends
    def test_get_place_trends(self):
        """Test getting the top 10 trending topics for a specific
        WOEID succeeds"""
        self.api.get_place_trends(id=1)

    def test_get_available_trends(self):
        """Test returning locations that Twitter has trending
        topic information for succeeds"""
        self.api.get_available_trends()

    def test_get_closest_trends(self):
        """Test getting the locations that Twitter has trending topic
        information for, closest to a specified location succeeds"""
        self.api.get_closest_trends(lat='37', long='-122')

    # Help
    def test_get_application_rate_limit_status(self):
        """Test getting application rate limit status succeeds"""
        self.oauth2_api.get_application_rate_limit_status()
