# -*- coding: utf-8 -*-

"""
twython.endpoints
~~~~~~~~~~~~~~~~~

This module provides a mixin for a :class:`Twython <Twython>` instance.
Parameters that need to be embedded in the API url just need to be passed
as a keyword argument.

e.g. Twython.retweet(id=12345)

This map is organized the order functions are documented at:
https://dev.twitter.com/docs/api/1.1
"""

import warnings

from .advisory import TwythonDeprecationWarning


class EndpointsMixin(object):
    # Timelines
    def get_mentions_timeline(self, **params):
        """Returns the 20 most recent mentions (tweets containing a users's
        @screen_name) for the authenticating user.

        Docs:
        https://dev.twitter.com/docs/api/1.1/get/statuses/mentions_timeline

        """
        return self.get('statuses/mentions_timeline', params=params)
    get_mentions_timeline.iter_mode = 'id'

    def get_user_timeline(self, **params):
        """Returns a collection of the most recent Tweets posted by the user
        indicated by the screen_name or user_id parameters.

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline

        """
        return self.get('statuses/user_timeline', params=params)
    get_user_timeline.iter_mode = 'id'

    def get_home_timeline(self, **params):
        """Returns a collection of the most recent Tweets and retweets
        posted by the authenticating user and the users they follow.

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline

        """
        return self.get('statuses/home_timeline', params=params)
    get_home_timeline.iter_mode = 'id'

    def retweeted_of_me(self, **params):
        """Returns the most recent tweets authored by the authenticating user
        that have been retweeted by others.

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/retweets_of_me

        """
        return self.get('statuses/retweets_of_me', params=params)
    retweeted_of_me.iter_mode = 'id'

    # Tweets
    def get_retweets(self, **params):
        """Returns up to 100 of the first retweets of a given tweet.

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/retweets/%3Aid

        """
        return self.get('statuses/retweets/%s' % params.get('id'),
                        params=params)

    def show_status(self, **params):
        """Returns a single Tweet, specified by the id parameter

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/show/%3Aid

        """
        return self.get('statuses/show/%s' % params.get('id'), params=params)

    def lookup_status(self, **params):
        """Returns fully-hydrated tweet objects for up to 100 tweets per
        request, as specified by comma-separated values passed to the id
        parameter.

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/lookup

        """
        return self.post('statuses/lookup', params=params)

    def destroy_status(self, **params):
        """Destroys the status specified by the required ID parameter

        Docs: https://dev.twitter.com/docs/api/1.1/post/statuses/destroy/%3Aid

        """
        return self.post('statuses/destroy/%s' % params.get('id'))

    def update_status(self, **params):
        """Updates the authenticating user's current status, also known as tweeting

        Docs: https://dev.twitter.com/docs/api/1.1/post/statuses/update

        """
        return self.post('statuses/update', params=params)

    def retweet(self, **params):
        """Retweets a tweet specified by the id parameter

        Docs: https://dev.twitter.com/docs/api/1.1/post/statuses/retweet/%3Aid

        """
        return self.post('statuses/retweet/%s' % params.get('id'))

    def update_status_with_media(self, **params):  # pragma: no cover
        """Updates the authenticating user's current status and attaches media
        for upload. In other words, it creates a Tweet with a picture attached.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/statuses/update_with_media

        """
        warnings.warn(
            'This method is deprecated. You should use Twython.upload_media instead.',
            TwythonDeprecationWarning,
            stacklevel=2
        )
        return self.post('statuses/update_with_media', params=params)

    def upload_media(self, **params):
        """Uploads media file to Twitter servers. The file will be available to be attached
        to a status for 60 minutes. To attach to a update, pass a list of returned media ids
        to the 'update_status' method using the 'media_ids' param.

        Docs:
        https://dev.twitter.com/rest/public/uploading-media-multiple-photos
        """
        return self.post('https://upload.twitter.com/1.1/media/upload.json', params=params)

    def get_oembed_tweet(self, **params):
        """Returns information allowing the creation of an embedded
        representation of a Tweet on third party sites.

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/oembed

        """
        return self.get('statuses/oembed', params=params)

    def get_retweeters_ids(self, **params):
        """Returns a collection of up to 100 user IDs belonging to users who
        have retweeted the tweet specified by the id parameter.

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/retweeters/ids

        """
        return self.get('statuses/retweeters/ids', params=params)
    get_retweeters_ids.iter_mode = 'cursor'
    get_retweeters_ids.iter_key = 'ids'

    # Search
    def search(self, **params):
        """Returns a collection of relevant Tweets matching a specified query.

        Docs: https://dev.twitter.com/docs/api/1.1/get/search/tweets

        """
        return self.get('search/tweets', params=params)
    search.iter_mode = 'id'
    search.iter_key = 'statuses'
    search.iter_metadata = 'search_metadata'

    # Direct Messages
    def get_direct_messages(self, **params):
        """Returns the 20 most recent direct messages sent to the authenticating user.

        Docs: https://dev.twitter.com/docs/api/1.1/get/direct_messages

        """
        return self.get('direct_messages', params=params)
    get_direct_messages.iter_mode = 'id'

    def get_sent_messages(self, **params):
        """Returns the 20 most recent direct messages sent by the authenticating user.

        Docs: https://dev.twitter.com/docs/api/1.1/get/direct_messages/sent

        """
        return self.get('direct_messages/sent', params=params)
    get_sent_messages.iter_mode = 'id'

    def get_direct_message(self, **params):
        """Returns a single direct message, specified by an id parameter.

        Docs: https://dev.twitter.com/docs/api/1.1/get/direct_messages/show

        """
        return self.get('direct_messages/show', params=params)

    def destroy_direct_message(self, **params):
        """Destroys the direct message specified in the required id parameter

        Docs: https://dev.twitter.com/docs/api/1.1/post/direct_messages/destroy

        """
        return self.post('direct_messages/destroy', params=params)

    def send_direct_message(self, **params):
        """Sends a new direct message to the specified user from the
        authenticating user.

        Docs: https://dev.twitter.com/docs/api/1.1/post/direct_messages/new

        """
        return self.post('direct_messages/new', params=params)

    # Friends & Followers
    def get_user_ids_of_blocked_retweets(self, **params):
        """Returns a collection of user_ids that the currently authenticated
        user does not want to receive retweets from.

        Docs:
        https://dev.twitter.com/docs/api/1.1/get/friendships/no_retweets/ids

        """
        return self.get('friendships/no_retweets/ids', params=params)

    def get_friends_ids(self, **params):
        """Returns a cursored collection of user IDs for every user the
        specified user is following (otherwise known as their "friends").

        Docs: https://dev.twitter.com/docs/api/1.1/get/friends/ids

        """
        return self.get('friends/ids', params=params)
    get_friends_ids.iter_mode = 'cursor'
    get_friends_ids.iter_key = 'ids'

    def get_followers_ids(self, **params):
        """Returns a cursored collection of user IDs for every user
        following the specified user.

        Docs: https://dev.twitter.com/docs/api/1.1/get/followers/ids

        """
        return self.get('followers/ids', params=params)
    get_followers_ids.iter_mode = 'cursor'
    get_followers_ids.iter_key = 'ids'

    def lookup_friendships(self, **params):
        """Returns the relationships of the authenticating user to the
        comma-separated list of up to 100 screen_names or user_ids provided.

        Docs: https://dev.twitter.com/docs/api/1.1/get/friendships/lookup

        """
        return self.get('friendships/lookup', params=params)

    def get_incoming_friendship_ids(self, **params):
        """Returns a collection of numeric IDs for every user who has a
        pending request to follow the authenticating user.

        Docs: https://dev.twitter.com/docs/api/1.1/get/friendships/incoming

        """
        return self.get('friendships/incoming', params=params)
    get_incoming_friendship_ids.iter_mode = 'cursor'
    get_incoming_friendship_ids.iter_key = 'ids'

    def get_outgoing_friendship_ids(self, **params):
        """Returns a collection of numeric IDs for every protected user for
        whom the authenticating user has a pending follow request.

        Docs: https://dev.twitter.com/docs/api/1.1/get/friendships/outgoing

        """
        return self.get('friendships/outgoing', params=params)
    get_outgoing_friendship_ids.iter_mode = 'cursor'
    get_outgoing_friendship_ids.iter_key = 'ids'

    def create_friendship(self, **params):
        """Allows the authenticating users to follow the user specified
        in the ID parameter.

        Docs: https://dev.twitter.com/docs/api/1.1/post/friendships/create

        """
        return self.post('friendships/create', params=params)

    def destroy_friendship(self, **params):
        """Allows the authenticating user to unfollow the user specified
        in the ID parameter.

        Docs: https://dev.twitter.com/docs/api/1.1/post/friendships/destroy

        """
        return self.post('friendships/destroy', params=params)

    def update_friendship(self, **params):
        """Allows one to enable or disable retweets and device notifications
        from the specified user.

        Docs: https://dev.twitter.com/docs/api/1.1/post/friendships/update

        """
        return self.post('friendships/update', params=params)

    def show_friendship(self, **params):
        """Returns detailed information about the relationship between two
        arbitrary users.

        Docs: https://dev.twitter.com/docs/api/1.1/get/friendships/show

        """
        return self.get('friendships/show', params=params)

    def get_friends_list(self, **params):
        """Returns a cursored collection of user objects for every user the
        specified user is following (otherwise known as their "friends").

        Docs: https://dev.twitter.com/docs/api/1.1/get/friends/list

        """
        return self.get('friends/list', params=params)
    get_friends_list.iter_mode = 'cursor'
    get_friends_list.iter_key = 'users'

    def get_followers_list(self, **params):
        """Returns a cursored collection of user objects for users
        following the specified user.

        Docs: https://dev.twitter.com/docs/api/1.1/get/followers/list

        """
        return self.get('followers/list', params=params)
    get_followers_list.iter_mode = 'cursor'
    get_followers_list.iter_key = 'users'

    # Users
    def get_account_settings(self, **params):
        """Returns settings (including current trend, geo and sleep time
        information) for the authenticating user.

        Docs: https://dev.twitter.com/docs/api/1.1/get/account/settings

        """
        return self.get('account/settings', params=params)

    def verify_credentials(self, **params):
        """Returns an HTTP 200 OK response code and a representation of the
        requesting user if authentication was successful; returns a 401 status
        code and an error message if not.

        Docs:
        https://dev.twitter.com/docs/api/1.1/get/account/verify_credentials

        """
        return self.get('account/verify_credentials', params=params)

    def update_account_settings(self, **params):
        """Updates the authenticating user's settings.

        Docs: https://dev.twitter.com/docs/api/1.1/post/account/settings

        """
        return self.post('account/settings', params=params)

    def update_delivery_service(self, **params):
        """Sets which device Twitter delivers updates to for the authenticating user.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_delivery_device

        """
        return self.post('account/update_delivery_device', params=params)

    def update_profile(self, **params):
        """Sets values that users are able to set under the "Account" tab of their
        settings page.

        Docs: https://dev.twitter.com/docs/api/1.1/post/account/update_profile

        """
        return self.post('account/update_profile', params=params)

    def update_profile_banner_image(self, **params):  # pragma: no cover
        """Updates the authenticating user's profile background image.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_profile_background_image

        """
        return self.post('account/update_profile_banner', params=params)

    def update_profile_colors(self, **params):
        """Sets one or more hex values that control the color scheme of the
        authenticating user's profile page on twitter.com.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_profile_colors

        """
        return self.post('account/update_profile_colors', params=params)

    def update_profile_image(self, **params):  # pragma: no cover
        """Updates the authenticating user's profile image.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_profile_image

        """
        return self.post('account/update_profile_image', params=params)

    def list_blocks(self, **params):
        """Returns a collection of user objects that the authenticating user
        is blocking.

        Docs: https://dev.twitter.com/docs/api/1.1/get/blocks/list

        """
        return self.get('blocks/list', params=params)
    list_blocks.iter_mode = 'cursor'
    list_blocks.iter_key = 'users'

    def list_block_ids(self, **params):
        """Returns an array of numeric user ids the authenticating user is blocking.

        Docs: https://dev.twitter.com/docs/api/1.1/get/blocks/ids

        """
        return self.get('blocks/ids', params=params)
    list_block_ids.iter_mode = 'cursor'
    list_block_ids.iter_key = 'ids'

    def create_block(self, **params):
        """Blocks the specified user from following the authenticating user.

        Docs: https://dev.twitter.com/docs/api/1.1/post/blocks/create

        """
        return self.post('blocks/create', params=params)

    def destroy_block(self, **params):
        """Un-blocks the user specified in the ID parameter for the
        authenticating user.

        Docs: https://dev.twitter.com/docs/api/1.1/post/blocks/destroy

        """
        return self.post('blocks/destroy', params=params)

    def lookup_user(self, **params):
        """Returns fully-hydrated user objects for up to 100 users per request,
        as specified by comma-separated values passed to the user_id and/or
        screen_name parameters.

        Docs: https://dev.twitter.com/docs/api/1.1/get/users/lookup

        """
        return self.post('users/lookup', params=params)

    def show_user(self, **params):
        """Returns a variety of information about the user specified by the
        required user_id or screen_name parameter.

        Docs: https://dev.twitter.com/docs/api/1.1/get/users/show

        """
        return self.get('users/show', params=params)

    def search_users(self, **params):
        """Provides a simple, relevance-based search interface to public user
        accounts on Twitter.

        Docs: https://dev.twitter.com/docs/api/1.1/get/users/search

        """
        return self.get('users/search', params=params)

    def get_contributees(self, **params):
        """Returns a collection of users that the specified user can "contribute" to.

        Docs: https://dev.twitter.com/docs/api/1.1/get/users/contributees

        """
        return self.get('users/contributees', params=params)

    def get_contributors(self, **params):
        """Returns a collection of users who can contribute to the specified account.

        Docs: https://dev.twitter.com/docs/api/1.1/get/users/contributors

        """
        return self.get('users/contributors', params=params)

    def remove_profile_banner(self, **params):
        """Removes the uploaded profile banner for the authenticating user.
        Returns HTTP 200 upon success.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/remove_profile_banner

        """
        return self.post('account/remove_profile_banner', params=params)

    def update_profile_background_image(self, **params):
        """Uploads a profile banner on behalf of the authenticating user.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_profile_banner

        """
        return self.post('account/update_profile_background_image',
                         params=params)

    def get_profile_banner_sizes(self, **params):
        """Returns a map of the available size variations of the specified
        user's profile banner.

        Docs: https://dev.twitter.com/docs/api/1.1/get/users/profile_banner

        """
        return self.get('users/profile_banner', params=params)

    # Suggested Users
    def get_user_suggestions_by_slug(self, **params):
        """Access the users in a given category of the Twitter suggested user list.

        Docs:
        https://dev.twitter.com/docs/api/1.1/get/users/suggestions/%3Aslug

        """
        return self.get('users/suggestions/%s' % params.get('slug'),
                        params=params)

    def get_user_suggestions(self, **params):
        """Access to Twitter's suggested user list.

        Docs: https://dev.twitter.com/docs/api/1.1/get/users/suggestions

        """
        return self.get('users/suggestions', params=params)

    def get_user_suggestions_statuses_by_slug(self, **params):
        """Access the users in a given category of the Twitter suggested user
        list and return their most recent status if they are not a protected
        user.

        Docs:
        https://dev.twitter.com/docs/api/1.1/get/users/suggestions/%3Aslug/members

        """
        return self.get('users/suggestions/%s/members' % params.get('slug'),
                        params=params)

    # Favorites
    def get_favorites(self, **params):
        """Returns the 20 most recent Tweets favorited by the authenticating
        or specified user.

        Docs: https://dev.twitter.com/docs/api/1.1/get/favorites/list

        """
        return self.get('favorites/list', params=params)
    get_favorites.iter_mode = 'id'

    def destroy_favorite(self, **params):
        """Un-favorites the status specified in the ID parameter as the
        authenticating user.

        Docs: https://dev.twitter.com/docs/api/1.1/post/favorites/destroy

        """
        return self.post('favorites/destroy', params=params)

    def create_favorite(self, **params):
        """Favorites the status specified in the ID parameter as the
        authenticating user.

        Docs: https://dev.twitter.com/docs/api/1.1/post/favorites/create

        """
        return self.post('favorites/create', params=params)

    # Lists
    def show_lists(self, **params):
        """Returns all lists the authenticating or specified user subscribes to,
        including their own.

        Docs: https://dev.twitter.com/docs/api/1.1/get/lists/list

        """
        return self.get('lists/list', params=params)

    def get_list_statuses(self, **params):
        """Returns a timeline of tweets authored by members of the specified list.

        Docs: https://dev.twitter.com/docs/api/1.1/get/lists/statuses

        """
        return self.get('lists/statuses', params=params)
    get_list_statuses.iter_mode = 'id'

    def delete_list_member(self, **params):
        """Removes the specified member from the list.

        Docs: https://dev.twitter.com/docs/api/1.1/post/lists/members/destroy

        """
        return self.post('lists/members/destroy', params=params)

    def get_list_memberships(self, **params):
        """Returns the lists the specified user has been added to.

        Docs: https://dev.twitter.com/docs/api/1.1/get/lists/memberships

        """
        return self.get('lists/memberships', params=params)
    get_list_memberships.iter_mode = 'cursor'
    get_list_memberships.iter_key = 'lists'

    def get_list_subscribers(self, **params):
        """Returns the subscribers of the specified list.

        Docs: https://dev.twitter.com/docs/api/1.1/get/lists/subscribers

        """
        return self.get('lists/subscribers', params=params)
    get_list_subscribers.iter_mode = 'cursor'
    get_list_subscribers.iter_key = 'users'

    def subscribe_to_list(self, **params):
        """Subscribes the authenticated user to the specified list.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/lists/subscribers/create

        """
        return self.post('lists/subscribers/create', params=params)

    def is_list_subscriber(self, **params):
        """Check if the specified user is a subscriber of the specified list.

        Docs: https://dev.twitter.com/docs/api/1.1/get/lists/subscribers/show

        """
        return self.get('lists/subscribers/show', params=params)

    def unsubscribe_from_list(self, **params):
        """Unsubscribes the authenticated user from the specified list.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/lists/subscribers/destroy

        """
        return self.post('lists/subscribers/destroy', params=params)

    def create_list_members(self, **params):
        """Adds multiple members to a list, by specifying a comma-separated
        list of member ids or screen names.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/lists/members/create_all

        """
        return self.post('lists/members/create_all', params=params)

    def is_list_member(self, **params):
        """Check if the specified user is a member of the specified list.

        Docs: https://dev.twitter.com/docs/api/1.1/get/lists/members/show

        """
        return self.get('lists/members/show', params=params)

    def get_list_members(self, **params):
        """Returns the members of the specified list.

        Docs: https://dev.twitter.com/docs/api/1.1/get/lists/members

        """
        return self.get('lists/members', params=params)
    get_list_members.iter_mode = 'cursor'
    get_list_members.iter_key = 'users'

    def add_list_member(self, **params):
        """Add a member to a list.

        Docs: https://dev.twitter.com/docs/api/1.1/post/lists/members/create

        """
        return self.post('lists/members/create', params=params)

    def delete_list(self, **params):
        """Deletes the specified list.

        Docs: https://dev.twitter.com/docs/api/1.1/post/lists/destroy

        """
        return self.post('lists/destroy', params=params)

    def update_list(self, **params):
        """Updates the specified list.

        Docs: https://dev.twitter.com/docs/api/1.1/post/lists/update

        """
        return self.post('lists/update', params=params)

    def create_list(self, **params):
        """Creates a new list for the authenticated user.

        Docs: https://dev.twitter.com/docs/api/1.1/post/lists/create

        """
        return self.post('lists/create', params=params)

    def get_specific_list(self, **params):
        """Returns the specified list.

        Docs: https://dev.twitter.com/docs/api/1.1/get/lists/show

        """
        return self.get('lists/show', params=params)

    def get_list_subscriptions(self, **params):
        """Obtain a collection of the lists the specified user is subscribed to.

        Docs: https://dev.twitter.com/docs/api/1.1/get/lists/subscriptions

        """
        return self.get('lists/subscriptions', params=params)
    get_list_subscriptions.iter_mode = 'cursor'
    get_list_subscriptions.iter_key = 'lists'

    def delete_list_members(self, **params):
        """Removes multiple members from a list, by specifying a
        comma-separated list of member ids or screen names.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/lists/members/destroy_all

        """
        return self.post('lists/members/destroy_all', params=params)

    def show_owned_lists(self, **params):
        """Returns the lists owned by the specified Twitter user.

        Docs: https://dev.twitter.com/docs/api/1.1/get/lists/ownerships

        """
        return self.get('lists/ownerships', params=params)
    show_owned_lists.iter_mode = 'cursor'
    show_owned_lists.iter_key = 'lists'

    # Saved Searches
    def get_saved_searches(self, **params):
        """Returns the authenticated user's saved search queries.

        Docs: https://dev.twitter.com/docs/api/1.1/get/saved_searches/list

        """
        return self.get('saved_searches/list', params=params)

    def show_saved_search(self, **params):
        """Retrieve the information for the saved search represented by the given id.

        Docs:
        https://dev.twitter.com/docs/api/1.1/get/saved_searches/show/%3Aid

        """
        return self.get('saved_searches/show/%s' % params.get('id'),
                        params=params)

    def create_saved_search(self, **params):
        """Create a new saved search for the authenticated user.

        Docs: https://dev.twitter.com/docs/api/1.1/post/saved_searches/create

        """
        return self.post('saved_searches/create', params=params)

    def destroy_saved_search(self, **params):
        """Destroys a saved search for the authenticating user.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/saved_searches/destroy/%3Aid

        """
        return self.post('saved_searches/destroy/%s' % params.get('id'),
                         params=params)

    # Places & Geo
    def get_geo_info(self, **params):
        """Returns all the information about a known place.

        Docs: https://dev.twitter.com/docs/api/1.1/get/geo/id/%3Aplace_id

        """
        return self.get('geo/id/%s' % params.get('place_id'), params=params)

    def reverse_geocode(self, **params):
        """Given a latitude and a longitude, searches for up to 20 places
        that can be used as a place_id when updating a status.

        Docs: https://dev.twitter.com/docs/api/1.1/get/geo/reverse_geocode

        """
        return self.get('geo/reverse_geocode', params=params)

    def search_geo(self, **params):
        """Search for places that can be attached to a statuses/update.

        Docs: https://dev.twitter.com/docs/api/1.1/get/geo/search

        """
        return self.get('geo/search', params=params)

    def get_similar_places(self, **params):
        """Locates places near the given coordinates which are similar in name.

        Docs: https://dev.twitter.com/docs/api/1.1/get/geo/similar_places

        """
        return self.get('geo/similar_places', params=params)

    def create_place(self, **params):  # pragma: no cover
        """Creates a new place object at the given latitude and longitude.

        Docs: https://dev.twitter.com/docs/api/1.1/post/geo/place

        """
        return self.post('geo/place', params=params)

    # Trends
    def get_place_trends(self, **params):
        """Returns the top 10 trending topics for a specific WOEID, if
        trending information is available for it.

        Docs: https://dev.twitter.com/docs/api/1.1/get/trends/place

        """
        return self.get('trends/place', params=params)

    def get_available_trends(self, **params):
        """Returns the locations that Twitter has trending topic information for.

        Docs: https://dev.twitter.com/docs/api/1.1/get/trends/available

        """
        return self.get('trends/available', params=params)

    def get_closest_trends(self, **params):
        """Returns the locations that Twitter has trending topic information
        for, closest to a specified location.

        Docs: https://dev.twitter.com/docs/api/1.1/get/trends/closest

        """
        return self.get('trends/closest', params=params)

    # Spam Reporting
    def report_spam(self, **params):  # pragma: no cover
        """Report the specified user as a spam account to Twitter.

        Docs: https://dev.twitter.com/docs/api/1.1/post/users/report_spam

        """
        return self.post('users/report_spam', params=params)

    # OAuth
    def invalidate_token(self, **params):  # pragma: no cover
        """Allows a registered application to revoke an issued OAuth 2 Bearer
        Token by presenting its client credentials.

        Docs: https://dev.twitter.com/docs/api/1.1/post/oauth2/invalidate_token

        """
        return self.post('oauth2/invalidate_token', params=params)

    # Help
    def get_twitter_configuration(self, **params):
        """Returns the current configuration used by Twitter

        Docs: https://dev.twitter.com/docs/api/1.1/get/help/configuration

        """
        return self.get('help/configuration', params=params)

    def get_supported_languages(self, **params):
        """Returns the list of languages supported by Twitter along with
        their ISO 639-1 code.

        Docs: https://dev.twitter.com/docs/api/1.1/get/help/languages

        """
        return self.get('help/languages', params=params)

    def get_privacy_policy(self, **params):
        """Returns Twitter's Privacy Policy

        Docs: https://dev.twitter.com/docs/api/1.1/get/help/privacy

        """
        return self.get('help/privacy', params=params)

    def get_tos(self, **params):
        """Return the Twitter Terms of Service

        Docs: https://dev.twitter.com/docs/api/1.1/get/help/tos

        """
        return self.get('help/tos', params=params)

    def get_application_rate_limit_status(self, **params):
        """Returns the current rate limits for methods belonging to the
        specified resource families.

        Docs:
        https://dev.twitter.com/docs/api/1.1/get/application/rate_limit_status

        """
        return self.get('application/rate_limit_status', params=params)


# from https://dev.twitter.com/docs/error-codes-responses
TWITTER_HTTP_STATUS_CODE = {
    200: ('OK', 'Success!'),
    304: ('Not Modified', 'There was no new data to return.'),
    400: ('Bad Request', 'The request was invalid. An accompanying \
          error message will explain why. This is the status code \
          will be returned during rate limiting.'),
    401: ('Unauthorized', 'Authentication credentials were missing \
          or incorrect.'),
    403: ('Forbidden', 'The request is understood, but it has been \
          refused. An accompanying error message will explain why. \
          This code is used when requests are being denied due to \
          update limits.'),
    404: ('Not Found', 'The URI requested is invalid or the resource \
          requested, such as a user, does not exists.'),
    406: ('Not Acceptable', 'Returned by the Search API when an \
          invalid format is specified in the request.'),
    410: ('Gone', 'This resource is gone. Used to indicate that an \
          API endpoint has been turned off.'),
    422: ('Unprocessable Entity', 'Returned when an image uploaded to \
          POST account/update_profile_banner is unable to be processed.'),
    429: ('Too Many Requests', 'Returned in API v1.1 when a request cannot \
          be served due to the application\'s rate limit having been \
          exhausted for the resource.'),
    500: ('Internal Server Error', 'Something is broken. Please post to the \
          group so the Twitter team can investigate.'),
    502: ('Bad Gateway', 'Twitter is down or being upgraded.'),
    503: ('Service Unavailable', 'The Twitter servers are up, but overloaded \
          with requests. Try again later.'),
    504: ('Gateway Timeout', 'The Twitter servers are up, but the request \
          couldn\'t be serviced due to some failure within our stack. Try \
          again later.'),
}
