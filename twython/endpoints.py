"""
A huge map of every Twitter API endpoint to a function definition in Twython.

Parameters that need to be embedded in the URL are treated with mustaches, e.g:

{{version}}, etc

When creating new endpoint definitions, keep in mind that the name of the mustache
will be replaced with the keyword that gets passed in to the function at call time.

i.e, in this case, if I pass version = 47 to any function, {{version}} will be replaced
with 47, instead of defaulting to 1.1 (said defaulting takes place at conversion time).

This map is organized the order functions are documented at:
https://dev.twitter.com/docs/api/1.1
"""

api_table = {
    # Timelines
    'get_mentions_timeline': {
        'url': '/statuses/mentions_timeline.json',
        'method': 'GET',
    },
    'get_user_timeline': {
        'url': '/statuses/user_timeline.json',
        'method': 'GET',
    },
    'get_home_timeline': {
        'url': '/statuses/home_timeline.json',
        'method': 'GET',
    },
    'retweeted_of_me': {
        'url': '/statuses/retweets_of_me.json',
        'method': 'GET',
    },


    # Tweets
    'get_retweets': {
        'url': '/statuses/retweets/{{id}}.json',
        'method': 'GET',
    },
    'show_status': {
        'url': '/statuses/show/{{id}}.json',
        'method': 'GET',
    },
    'destroy_status': {
        'url': '/statuses/destroy/{{id}}.json',
        'method': 'POST',
    },
    'update_status': {
        'url': '/statuses/update.json',
        'method': 'POST',
    },
    'retweet': {
        'url': '/statuses/retweet/{{id}}.json',
        'method': 'POST',
    },
    'update_status_with_media': {
        'url': '/statuses/update_with_media.json',
        'method': 'POST',
    },
    'get_oembed_tweet': {
        'url': '/statuses/oembed.json',
        'method': 'GET',
    },
    'get_retweeters_ids': {
        'url': '/statuses/retweeters/ids.json',
        'method': 'GET',
    },


    # Search
    'search': {
        'url': '/search/tweets.json',
        'method': 'GET',
    },


    # Direct Messages
    'get_direct_messages': {
        'url': '/direct_messages.json',
        'method': 'GET',
    },
    'get_sent_messages': {
        'url': '/direct_messages/sent.json',
        'method': 'GET',
    },
    'get_direct_message': {
        'url': '/direct_messages/show.json',
        'method': 'GET',
    },
    'destroy_direct_message': {
        'url': '/direct_messages/destroy.json',
        'method': 'POST',
    },
    'send_direct_message': {
        'url': '/direct_messages/new.json',
        'method': 'POST',
    },


    # Friends & Followers
    'get_user_ids_of_blocked_retweets': {
        'url': '/friendships/no_retweets/ids.json',
        'method': 'GET',
    },
    'get_friends_ids': {
        'url': '/friends/ids.json',
        'method': 'GET',
    },
    'get_followers_ids': {
        'url': '/followers/ids.json',
        'method': 'GET',
    },
    'lookup_friendships': {
        'url': '/friendships/lookup.json',
        'method': 'GET',
    },
    'get_incoming_friendship_ids': {
        'url': '/friendships/incoming.json',
        'method': 'GET',
    },
    'get_outgoing_friendship_ids': {
        'url': '/friendships/outgoing.json',
        'method': 'GET',
    },
    'create_friendship': {
        'url': '/friendships/create.json',
        'method': 'POST',
    },
    'destroy_friendship': {
        'url': '/friendships/destroy.json',
        'method': 'POST',
    },
    'update_friendship': {
        'url': '/friendships/update.json',
        'method': 'POST',
    },
    'show_friendship': {
        'url': '/friendships/show.json',
        'method': 'GET',
    },
    'get_friends_list': {
        'url': '/friends/list.json',
        'method': 'GET',
    },
    'get_followers_list': {
        'url': '/followers/list.json',
        'method': 'GET',
    },


    # Users
    'get_account_settings': {
        'url': '/account/settings.json',
        'method': 'GET',
    },
    'verify_credentials': {
        'url': '/account/verify_credentials.json',
        'method': 'GET',
    },
    'update_account_settings': {
        'url': '/account/settings.json',
        'method': 'POST',
    },
    'update_delivery_service': {
        'url': '/account/update_delivery_device.json',
        'method': 'POST',
    },
    'update_profile': {
        'url': '/account/update_profile.json',
        'method': 'POST',
    },
    'update_profile_background_image': {
        'url': '/account/update_profile_banner.json',
        'method': 'POST',
    },
    'update_profile_colors': {
        'url': '/account/update_profile_colors.json',
        'method': 'POST',
    },
    'update_profile_image': {
        'url': '/account/update_profile_image.json',
        'method': 'POST',
    },
    'list_blocks': {
        'url': '/blocks/list.json',
        'method': 'GET',
    },
    'list_block_ids': {
        'url': '/blocks/ids.json',
        'method': 'GET',
    },
    'create_block': {
        'url': '/blocks/create.json',
        'method': 'POST',
    },
    'destroy_block': {
        'url': '/blocks/destroy.json',
        'method': 'POST',
    },
    'lookup_user': {
        'url': '/users/lookup.json',
        'method': 'GET',
    },
    'show_user': {
        'url': '/users/show.json',
        'method': 'GET',
    },
    'search_users': {
        'url': '/users/search.json',
        'method': 'GET',
    },
    'get_contributees': {
        'url': '/users/contributees.json',
        'method': 'GET',
    },
    'get_contributors': {
        'url': '/users/contributors.json',
        'method': 'GET',
    },
    'remove_profile_banner': {
        'url': '/account/remove_profile_banner.json',
        'method': 'POST',
    },
    'update_profile_background_image': {
        'url': '/account/update_profile_background_image.json',
        'method': 'POST',
    },
    'get_profile_banner_sizes': {
        'url': '/users/profile_banner.json',
        'method': 'GET',
    },


    # Suggested Users
    'get_user_suggestions_by_slug': {
        'url': '/users/suggestions/{{slug}}.json',
        'method': 'GET',
    },
    'get_user_suggestions': {
        'url': '/users/suggestions.json',
        'method': 'GET',
    },
    'get_user_suggestions_statuses_by_slug': {
        'url': '/users/suggestions/{{slug}}/members.json',
        'method': 'GET',
    },


    # Favorites
    'get_favorites': {
        'url': '/favorites/list.json',
        'method': 'GET',
    },
    'destroy_favorite': {
        'url': '/favorites/destroy.json',
        'method': 'POST',
    },
    'create_favorite': {
        'url': '/favorites/create.json',
        'method': 'POST',
    },


    # Lists
    'show_lists': {
        'url': '/lists/list.json',
        'method': 'GET',
    },
    'get_list_statuses': {
        'url': '/lists/statuses.json',
        'method': 'GET'
    },
    'delete_list_member': {
        'url': '/lists/members/destroy.json',
        'method': 'POST',
    },
    'get_list_memberships': {
        'url': '/lists/memberships.json',
        'method': 'GET',
    },
    'get_list_subscribers': {
        'url': '/lists/subscribers.json',
        'method': 'GET',
    },
    'subscribe_to_list': {
        'url': '/lists/subscribers/create.json',
        'method': 'POST',
    },
    'is_list_subscriber': {
        'url': '/lists/subscribers/show.json',
        'method': 'GET',
    },
    'unsubscribe_from_list': {
        'url': '/lists/subscribers/destroy.json',
        'method': 'POST',
    },
    'create_list_members': {
        'url': '/lists/members/create_all.json',
        'method': 'POST'
    },
    'is_list_member': {
        'url': '/lists/members/show.json',
        'method': 'GET',
    },
    'get_list_members': {
        'url': '/lists/members.json',
        'method': 'GET',
    },
    'add_list_member': {
        'url': '/lists/members/create.json',
        'method': 'POST',
    },
    'delete_list': {
        'url': '/lists/destroy.json',
        'method': 'POST',
    },
    'update_list': {
        'url': '/lists/update.json',
        'method': 'POST',
    },
    'create_list': {
        'url': '/lists/create.json',
        'method': 'POST',
    },
    'get_specific_list': {
        'url': '/lists/show.json',
        'method': 'GET',
    },
    'get_list_subscriptions': {
        'url': '/lists/subscriptions.json',
        'method': 'GET',
    },
    'delete_list_members': {
        'url': '/lists/members/destroy_all.json',
        'method': 'POST'
    },
    'show_owned_lists': {
        'url': '/lists/ownerships.json',
        'method': 'GET'
    },


    # Saved Searches
    'get_saved_searches': {
        'url': '/saved_searches/list.json',
        'method': 'GET',
    },
    'show_saved_search': {
        'url': '/saved_searches/show/{{id}}.json',
        'method': 'GET',
    },
    'create_saved_search': {
        'url': '/saved_searches/create.json',
        'method': 'POST',
    },
    'destroy_saved_search': {
        'url': '/saved_searches/destroy/{{id}}.json',
        'method': 'POST',
    },


    # Places & Geo
    'get_geo_info': {
        'url': '/geo/id/{{place_id}}.json',
        'method': 'GET',
    },
    'reverse_geocode': {
        'url': '/geo/reverse_geocode.json',
        'method': 'GET',
    },
    'search_geo': {
        'url': '/geo/search.json',
        'method': 'GET',
    },
    'get_similar_places': {
        'url': '/geo/similar_places.json',
        'method': 'GET',
    },
    'create_place': {
        'url': '/geo/place.json',
        'method': 'POST',
    },


    # Trends
    'get_place_trends': {
        'url': '/trends/place.json',
        'method': 'GET',
    },
    'get_available_trends': {
        'url': '/trends/available.json',
        'method': 'GET',
    },
    'get_closest_trends': {
        'url': '/trends/closest.json',
        'method': 'GET',
    },


    # Spam Reporting
    'report_spam': {
        'url': '/users/report_spam.json',
        'method': 'POST',
    },
}


# from https://dev.twitter.com/docs/error-codes-responses
twitter_http_status_codes = {
    200: ('OK', 'Success!'),
    304: ('Not Modified', 'There was no new data to return.'),
    400: ('Bad Request', 'The request was invalid. An accompanying error message will explain why. This is the status code will be returned during rate limiting.'),
    401: ('Unauthorized', 'Authentication credentials were missing or incorrect.'),
    403: ('Forbidden', 'The request is understood, but it has been refused. An accompanying error message will explain why. This code is used when requests are being denied due to update limits.'),
    404: ('Not Found', 'The URI requested is invalid or the resource requested, such as a user, does not exists.'),
    406: ('Not Acceptable', 'Returned by the Search API when an invalid format is specified in the request.'),
    410: ('Gone', 'This resource is gone. Used to indicate that an API endpoint has been turned off.'),
    422: ('Unprocessable Entity', 'Returned when an image uploaded to POST account/update_profile_banner is unable to be processed.'),
    429: ('Too Many Requests', 'Returned in API v1.1 when a request cannot be served due to the application\'s rate limit having been exhausted for the resource.'),
    500: ('Internal Server Error', 'Something is broken. Please post to the group so the Twitter team can investigate.'),
    502: ('Bad Gateway', 'Twitter is down or being upgraded.'),
    503: ('Service Unavailable', 'The Twitter servers are up, but overloaded with requests. Try again later.'),
    504: ('Gateway Timeout', 'The Twitter servers are up, but the request couldn\'t be serviced due to some failure within our stack. Try again later.'),
}
