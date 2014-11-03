from twython import Twython, TwythonError, TwythonAuthError

from .config import (
    app_key, app_secret, oauth_token, oauth_token_secret,
    protected_twitter_1, protected_twitter_2, screen_name,
    test_tweet_id, test_list_slug, test_list_owner_screen_name,
    access_token, test_tweet_object, test_tweet_html, unittest
)

import time


class TwythonEndpointsTestCase(unittest.TestCase):
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

        self.api = Twython(app_key, app_secret,
                           oauth_token, oauth_token_secret,
                           client_args=client_args)

        self.oauth2_api = Twython(app_key, access_token=access_token,
                                  client_args=oauth2_client_args)

    # Timelines
    @unittest.skip('skipping non-updated test')
    def test_get_mentions_timeline(self):
        """Test returning mentions timeline for authenticated user succeeds"""
        self.api.get_mentions_timeline()

    @unittest.skip('skipping non-updated test')
    def test_get_user_timeline(self):
        """Test returning timeline for authenticated user and random user
        succeeds"""
        self.api.get_user_timeline()  # Authenticated User Timeline
        self.api.get_user_timeline(screen_name='twitter')
        # Random User Timeline

    @unittest.skip('skipping non-updated test')
    def test_get_protected_user_timeline_following(self):
        """Test returning a protected user timeline who you are following
        succeeds"""
        self.api.get_user_timeline(screen_name=protected_twitter_1)

    @unittest.skip('skipping non-updated test')
    def test_get_protected_user_timeline_not_following(self):
        """Test returning a protected user timeline who you are not following
        fails and raise a TwythonAuthError"""
        self.assertRaises(TwythonAuthError, self.api.get_user_timeline,
                          screen_name=protected_twitter_2)

    @unittest.skip('skipping non-updated test')
    def test_retweeted_of_me(self):
        """Test that getting recent tweets by authenticated user that have
        been retweeted by others succeeds"""
        self.api.retweeted_of_me()

    @unittest.skip('skipping non-updated test')
    def test_get_home_timeline(self):
        """Test returning home timeline for authenticated user succeeds"""
        self.api.get_home_timeline()

    # Tweets
    @unittest.skip('skipping non-updated test')
    def test_get_retweets(self):
        """Test getting retweets of a specific tweet succeeds"""
        self.api.get_retweets(id=test_tweet_id)

    @unittest.skip('skipping non-updated test')
    def test_show_status(self):
        """Test returning a single status details succeeds"""
        self.api.show_status(id=test_tweet_id)

    @unittest.skip('skipping non-updated test')
    def test_update_and_destroy_status(self):
        """Test updating and deleting a status succeeds"""
        status = self.api.update_status(status='Test post just to get \
                    deleted :( %s' % int(time.time()))
        self.api.destroy_status(id=status['id_str'])

    @unittest.skip('skipping non-updated test')
    def test_get_oembed_tweet(self):
        """Test getting info to embed tweet on Third Party site succeeds"""
        self.api.get_oembed_tweet(id='99530515043983360')

    @unittest.skip('skipping non-updated test')
    def test_get_retweeters_ids(self):
        """Test getting ids for people who retweeted a tweet succeeds"""
        self.api.get_retweeters_ids(id='99530515043983360')

    # Search
    @unittest.skip('skipping non-updated test')
    def test_search(self):
        """Test searching tweets succeeds"""
        self.api.search(q='twitter')

    # Direct Messages
    @unittest.skip('skipping non-updated test')
    def test_get_direct_messages(self):
        """Test getting the authenticated users direct messages succeeds"""
        self.api.get_direct_messages()

    @unittest.skip('skipping non-updated test')
    def test_get_sent_messages(self):
        """Test getting the authenticated users direct messages they've
        sent succeeds"""
        self.api.get_sent_messages()

    @unittest.skip('skipping non-updated test')
    def test_send_get_and_destroy_direct_message(self):
        """Test sending, getting, then destory a direct message succeeds"""
        message = self.api.send_direct_message(screen_name=protected_twitter_1,
                                               text='Hey d00d! %s\
                                               ' % int(time.time()))

        self.api.get_direct_message(id=message['id_str'])
        self.api.destroy_direct_message(id=message['id_str'])

    @unittest.skip('skipping non-updated test')
    def test_send_direct_message_to_non_follower(self):
        """Test sending a direct message to someone who doesn't follow you
        fails"""
        self.assertRaises(TwythonError, self.api.send_direct_message,
                          screen_name=protected_twitter_2, text='Yo, man! \
                          %s' % int(time.time()))

    # Friends & Followers
    @unittest.skip('skipping non-updated test')
    def test_get_user_ids_of_blocked_retweets(self):
        """Test that collection of user_ids that the authenticated user does
        not want to receive retweets from succeeds"""
        self.api.get_user_ids_of_blocked_retweets(stringify_ids=True)

    @unittest.skip('skipping non-updated test')
    def test_get_friends_ids(self):
        """Test returning ids of users the authenticated user and then a random
        user is following succeeds"""
        self.api.get_friends_ids()
        self.api.get_friends_ids(screen_name='twitter')

    @unittest.skip('skipping non-updated test')
    def test_get_followers_ids(self):
        """Test returning ids of users the authenticated user and then a random
        user are followed by succeeds"""
        self.api.get_followers_ids()
        self.api.get_followers_ids(screen_name='twitter')

    @unittest.skip('skipping non-updated test')
    def test_lookup_friendships(self):
        """Test returning relationships of the authenticating user to the
        comma-separated list of up to 100 screen_names or user_ids provided
        succeeds"""
        self.api.lookup_friendships(screen_name='twitter,ryanmcgrath')

    @unittest.skip('skipping non-updated test')
    def test_get_incoming_friendship_ids(self):
        """Test returning incoming friendship ids succeeds"""
        self.api.get_incoming_friendship_ids()

    @unittest.skip('skipping non-updated test')
    def test_get_outgoing_friendship_ids(self):
        """Test returning outgoing friendship ids succeeds"""
        self.api.get_outgoing_friendship_ids()

    @unittest.skip('skipping non-updated test')
    def test_create_friendship(self):
        """Test creating a friendship succeeds"""
        self.api.create_friendship(screen_name='justinbieber')

    @unittest.skip('skipping non-updated test')
    def test_destroy_friendship(self):
        """Test destroying a friendship succeeds"""
        self.api.destroy_friendship(screen_name='justinbieber')

    @unittest.skip('skipping non-updated test')
    def test_update_friendship(self):
        """Test updating friendships succeeds"""
        self.api.update_friendship(screen_name=protected_twitter_1,
                                   retweets='true')

        self.api.update_friendship(screen_name=protected_twitter_1,
                                   retweets=False)

    @unittest.skip('skipping non-updated test')
    def test_show_friendships(self):
        """Test showing specific friendship succeeds"""
        self.api.show_friendship(target_screen_name=protected_twitter_1)

    @unittest.skip('skipping non-updated test')
    def test_get_friends_list(self):
        """Test getting list of users authenticated user then random user is
        following succeeds"""
        self.api.get_friends_list()
        self.api.get_friends_list(screen_name='twitter')

    @unittest.skip('skipping non-updated test')
    def test_get_followers_list(self):
        """Test getting list of users authenticated user then random user are
        followed by succeeds"""
        self.api.get_followers_list()
        self.api.get_followers_list(screen_name='twitter')

    # Users
    @unittest.skip('skipping non-updated test')
    def test_get_account_settings(self):
        """Test getting the authenticated user account settings succeeds"""
        self.api.get_account_settings()

    @unittest.skip('skipping non-updated test')
    def test_verify_credentials(self):
        """Test representation of the authenticated user call succeeds"""
        self.api.verify_credentials()

    @unittest.skip('skipping non-updated test')
    def test_update_account_settings(self):
        """Test updating a user account settings succeeds"""
        self.api.update_account_settings(lang='en')

    @unittest.skip('skipping non-updated test')
    def test_update_delivery_service(self):
        """Test updating delivery settings fails because we don't have
        a mobile number on the account"""
        self.assertRaises(TwythonError, self.api.update_delivery_service,
                          device='none')

    @unittest.skip('skipping non-updated test')
    def test_update_profile(self):
        """Test updating profile succeeds"""
        self.api.update_profile(include_entities='true')

    @unittest.skip('skipping non-updated test')
    def test_update_profile_colors(self):
        """Test updating profile colors succeeds"""
        self.api.update_profile_colors(profile_background_color='3D3D3D')

    @unittest.skip('skipping non-updated test')
    def test_list_blocks(self):
        """Test listing users who are blocked by the authenticated user
        succeeds"""
        self.api.list_blocks()

    @unittest.skip('skipping non-updated test')
    def test_list_block_ids(self):
        """Test listing user ids who are blocked by the authenticated user
        succeeds"""
        self.api.list_block_ids()

    @unittest.skip('skipping non-updated test')
    def test_create_block(self):
        """Test blocking a user succeeds"""
        self.api.create_block(screen_name='justinbieber')

    @unittest.skip('skipping non-updated test')
    def test_destroy_block(self):
        """Test unblocking a user succeeds"""
        self.api.destroy_block(screen_name='justinbieber')

    @unittest.skip('skipping non-updated test')
    def test_lookup_user(self):
        """Test listing a number of user objects succeeds"""
        self.api.lookup_user(screen_name='twitter,justinbieber')

    @unittest.skip('skipping non-updated test')
    def test_show_user(self):
        """Test showing one user works"""
        self.api.show_user(screen_name='twitter')

    @unittest.skip('skipping non-updated test')
    def test_search_users(self):
        """Test that searching for users succeeds"""
        self.api.search_users(q='Twitter API')

    @unittest.skip('skipping non-updated test')
    def test_get_contributees(self):
        """Test returning list of accounts the specified user can
        contribute to succeeds"""
        self.api.get_contributees(screen_name='TechCrunch')

    @unittest.skip('skipping non-updated test')
    def test_get_contributors(self):
        """Test returning list of accounts that contribute to the
        authenticated user fails because we are not a Contributor account"""
        self.assertRaises(TwythonError, self.api.get_contributors,
                          screen_name=screen_name)

    @unittest.skip('skipping non-updated test')
    def test_remove_profile_banner(self):
        """Test removing profile banner succeeds"""
        self.api.remove_profile_banner()

    @unittest.skip('skipping non-updated test')
    def test_get_profile_banner_sizes(self):
        """Test getting list of profile banner sizes fails because
        we have not uploaded a profile banner"""
        self.assertRaises(TwythonError, self.api.get_profile_banner_sizes)

    @unittest.skip('skipping non-updated test')
    def test_list_mutes(self):
        """Test listing users who are muted by the authenticated user
        succeeds"""
        self.api.list_mutes()

    @unittest.skip('skipping non-updated test')
    def test_list_mute_ids(self):
        """Test listing user ids who are muted by the authenticated user
        succeeds"""
        self.api.list_mute_ids()

    @unittest.skip('skipping non-updated test')
    def test_create_mute(self):
        """Test muting a user succeeds"""
        self.api.create_mute(screen_name='justinbieber')

    @unittest.skip('skipping non-updated test')
    def test_destroy_mute(self):
        """Test muting a user succeeds"""
        self.api.destroy_mute(screen_name='justinbieber')

    # Suggested Users
    @unittest.skip('skipping non-updated test')
    def test_get_user_suggestions_by_slug(self):
        """Test getting user suggestions by slug succeeds"""
        self.api.get_user_suggestions_by_slug(slug='twitter')

    @unittest.skip('skipping non-updated test')
    def test_get_user_suggestions(self):
        """Test getting user suggestions succeeds"""
        self.api.get_user_suggestions()

    @unittest.skip('skipping non-updated test')
    def test_get_user_suggestions_statuses_by_slug(self):
        """Test getting status of suggested users succeeds"""
        self.api.get_user_suggestions_statuses_by_slug(slug='funny')

    # Favorites
    @unittest.skip('skipping non-updated test')
    def test_get_favorites(self):
        """Test getting list of favorites for the authenticated
        user succeeds"""
        self.api.get_favorites()

    @unittest.skip('skipping non-updated test')
    def test_create_and_destroy_favorite(self):
        """Test creating and destroying a favorite on a tweet succeeds"""
        self.api.create_favorite(id=test_tweet_id)
        self.api.destroy_favorite(id=test_tweet_id)

    # Lists
    @unittest.skip('skipping non-updated test')
    def test_show_lists(self):
        """Test show lists for specified user"""
        self.api.show_lists(screen_name='twitter')

    @unittest.skip('skipping non-updated test')
    def test_get_list_statuses(self):
        """Test timeline of tweets authored by members of the
        specified list succeeds"""
        self.api.get_list_statuses(slug=test_list_slug,
                                   owner_screen_name=test_list_owner_screen_name)

    @unittest.skip('skipping non-updated test')
    def test_create_update_destroy_list_add_remove_list_members(self):
        """Test create a list, adding and removing members then
        deleting the list succeeds"""
        the_list = self.api.create_list(name='Stuff %s' % int(time.time()))
        list_id = the_list['id_str']

        self.api.update_list(list_id=list_id, name='Stuff Renamed \
                             %s' % int(time.time()))

        screen_names = ['johncena', 'xbox']
        # Multi add/delete members
        self.api.create_list_members(list_id=list_id,
                                     screen_name=screen_names)
        self.api.delete_list_members(list_id=list_id,
                                     screen_name=screen_names)

        # Single add/delete member
        self.api.add_list_member(list_id=list_id, screen_name='justinbieber')
        self.api.delete_list_member(list_id=list_id,
                                    screen_name='justinbieber')

        self.api.delete_list(list_id=list_id)

    @unittest.skip('skipping non-updated test')
    def test_get_list_memberships(self):
        """Test list of memberhips the authenticated user succeeds"""
        self.api.get_list_memberships()

    @unittest.skip('skipping non-updated test')
    def test_get_list_subscribers(self):
        """Test list of subscribers of a specific list succeeds"""
        self.api.get_list_subscribers(slug=test_list_slug,
                                      owner_screen_name=test_list_owner_screen_name)

    @unittest.skip('skipping non-updated test')
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

    @unittest.skip('skipping non-updated test')
    def test_is_list_member(self):
        """Test returning if specified user is member of a list succeeds"""
        # Returns 404 if not list member
        self.api.is_list_member(slug=test_list_slug,
                                owner_screen_name=test_list_owner_screen_name,
                                screen_name='themattharris')

    @unittest.skip('skipping non-updated test')
    def test_get_list_members(self):
        """Test listing members of the specified list succeeds"""
        self.api.get_list_members(slug=test_list_slug,
                                  owner_screen_name=test_list_owner_screen_name)

    @unittest.skip('skipping non-updated test')
    def test_get_specific_list(self):
        """Test getting specific list succeeds"""
        self.api.get_specific_list(slug=test_list_slug,
                                   owner_screen_name=test_list_owner_screen_name)

    @unittest.skip('skipping non-updated test')
    def test_get_list_subscriptions(self):
        """Test collection of the lists the specified user is
        subscribed to succeeds"""
        self.api.get_list_subscriptions(screen_name='twitter')

    @unittest.skip('skipping non-updated test')
    def test_show_owned_lists(self):
        """Test collection of lists the specified user owns succeeds"""
        self.api.show_owned_lists(screen_name='twitter')

    # Saved Searches
    @unittest.skip('skipping non-updated test')
    def test_get_saved_searches(self):
        """Test getting list of saved searches for authenticated
        user succeeds"""
        self.api.get_saved_searches()

    @unittest.skip('skipping non-updated test')
    def test_create_get_destroy_saved_search(self):
        """Test getting list of saved searches for authenticated
        user succeeds"""
        saved_search = self.api.create_saved_search(query='#Twitter')
        saved_search_id = saved_search['id_str']

        self.api.show_saved_search(id=saved_search_id)
        self.api.destroy_saved_search(id=saved_search_id)

    # Places & Geo
    @unittest.skip('skipping non-updated test')
    def test_get_geo_info(self):
        """Test getting info about a geo location succeeds"""
        self.api.get_geo_info(place_id='df51dec6f4ee2b2c')

    @unittest.skip('skipping non-updated test')
    def test_reverse_geo_code(self):
        """Test reversing geocode succeeds"""
        self.api.reverse_geocode(lat='37.76893497', long='-122.42284884')

    @unittest.skip('skipping non-updated test')
    def test_search_geo(self):
        """Test search for places that can be attached
        to a statuses/update succeeds"""
        self.api.search_geo(query='Toronto')

    @unittest.skip('skipping non-updated test')
    def test_get_similar_places(self):
        """Test locates places near the given coordinates which
        are similar in name succeeds"""
        self.api.get_similar_places(lat='37', long='-122', name='Twitter HQ')

    # Trends
    @unittest.skip('skipping non-updated test')
    def test_get_place_trends(self):
        """Test getting the top 10 trending topics for a specific
        WOEID succeeds"""
        self.api.get_place_trends(id=1)

    @unittest.skip('skipping non-updated test')
    def test_get_available_trends(self):
        """Test returning locations that Twitter has trending
        topic information for succeeds"""
        self.api.get_available_trends()

    @unittest.skip('skipping non-updated test')
    def test_get_closest_trends(self):
        """Test getting the locations that Twitter has trending topic
        information for, closest to a specified location succeeds"""
        self.api.get_closest_trends(lat='37', long='-122')

    # Help
    @unittest.skip('skipping non-updated test')
    def test_get_twitter_configuration(self):
        """Test getting Twitter's configuration succeeds"""
        self.api.get_twitter_configuration()

    @unittest.skip('skipping non-updated test')
    def test_get_supported_languages(self):
        """Test getting languages supported by Twitter succeeds"""
        self.api.get_supported_languages()

    @unittest.skip('skipping non-updated test')
    def test_privacy_policy(self):
        """Test getting Twitter's Privacy Policy succeeds"""
        self.api.get_privacy_policy()

    @unittest.skip('skipping non-updated test')
    def test_get_tos(self):
        """Test getting the Twitter Terms of Service succeeds"""
        self.api.get_tos()

    @unittest.skip('skipping non-updated test')
    def test_get_application_rate_limit_status(self):
        """Test getting application rate limit status succeeds"""
        self.oauth2_api.get_application_rate_limit_status()
