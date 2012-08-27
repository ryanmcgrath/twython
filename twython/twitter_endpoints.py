"""
    A huge map of every Twitter API endpoint to a function definition in Twython.

    Parameters that need to be embedded in the URL are treated with mustaches, e.g:

    {{version}}, etc

    When creating new endpoint definitions, keep in mind that the name of the mustache
    will be replaced with the keyword that gets passed in to the function at call time.

    i.e, in this case, if I pass version = 47 to any function, {{version}} will be replaced
    with 47, instead of defaulting to 1 (said defaulting takes place at conversion time).
"""

# Base Twitter API url, no need to repeat this junk...
base_url = 'http://api.twitter.com/{{version}}'

api_table = {
    'getRateLimitStatus': {
        'url': '/account/rate_limit_status.json',
        'method': 'GET',
    },

    'verifyCredentials': {
        'url': '/account/verify_credentials.json',
        'method': 'GET',
    },

    'endSession': {
        'url': '/account/end_session.json',
        'method': 'POST',
    },

    # Timeline methods
    'getHomeTimeline': {
        'url': '/statuses/home_timeline.json',
        'method': 'GET',
    },
    'getUserTimeline': {
        'url': '/statuses/user_timeline.json',
        'method': 'GET',
    },

    # Interfacing with friends/followers
    'getUserMentions': {
        'url': '/statuses/mentions.json',
        'method': 'GET',
    },
    'createFriendship': {
        'url': '/friendships/create.json',
        'method': 'POST',
    },
    'destroyFriendship': {
        'url': '/friendships/destroy.json',
        'method': 'POST',
    },
    'getFriendsIDs': {
        'url': '/friends/ids.json',
        'method': 'GET',
    },
    'getFollowersIDs': {
        'url': '/followers/ids.json',
        'method': 'GET',
    },
    'getIncomingFriendshipIDs': {
        'url': '/friendships/incoming.json',
        'method': 'GET',
    },
    'getOutgoingFriendshipIDs': {
        'url': '/friendships/outgoing.json',
        'method': 'GET',
    },

    # Retweets
    'reTweet': {
        'url': '/statuses/retweet/{{id}}.json',
        'method': 'POST',
    },
    'getRetweets': {
        'url': '/statuses/retweets/{{id}}.json',
        'method': 'GET',
    },
    'retweetedOfMe': {
        'url': '/statuses/retweets_of_me.json',
        'method': 'GET',
    },
    'retweetedByMe': {
        'url': '/statuses/retweeted_by_me.json',
        'method': 'GET',
    },
    'retweetedToMe': {
        'url': '/statuses/retweeted_to_me.json',
        'method': 'GET',
    },

    # User methods
    'showUser': {
        'url': '/users/show.json',
        'method': 'GET',
    },
    'searchUsers': {
        'url': '/users/search.json',
        'method': 'GET',
    },

    'lookupUser': {
        'url': '/users/lookup.json',
        'method': 'GET',
    },

    # Status methods - showing, updating, destroying, etc.
    'showStatus': {
        'url': '/statuses/show.json',
        'method': 'GET',
    },
    'updateStatus': {
        'url': '/statuses/update.json',
        'method': 'POST',
    },
    'destroyStatus': {
        'url': '/statuses/destroy/{{id}}.json',
        'method': 'POST',
    },

    # Direct Messages - getting, sending, effing, etc.
    'getDirectMessages': {
        'url': '/direct_messages.json',
        'method': 'GET',
    },
    'getSentMessages': {
        'url': '/direct_messages/sent.json',
        'method': 'GET',
    },
    'sendDirectMessage': {
        'url': '/direct_messages/new.json',
        'method': 'POST',
    },
    'destroyDirectMessage': {
        'url': '/direct_messages/destroy/{{id}}.json',
        'method': 'POST',
    },

    # Friendship methods
    'checkIfFriendshipExists': {
        'url': '/friendships/exists.json',
        'method': 'GET',
    },
    'showFriendship': {
        'url': '/friendships/show.json',
        'method': 'GET',
    },

    # Profile methods
    'updateProfile': {
        'url': '/account/update_profile.json',
        'method': 'POST',
    },
    'updateProfileColors': {
        'url': '/account/update_profile_colors.json',
        'method': 'POST',
    },
    'myTotals': {
        'url' : '/account/totals.json',
        'method': 'GET',
    },

    # Favorites methods
    'getFavorites': {
        'url': '/favorites.json',
        'method': 'GET',
    },
    'createFavorite': {
        'url': '/favorites/create/{{id}}.json',
        'method': 'POST',
    },
    'destroyFavorite': {
        'url': '/favorites/destroy/{{id}}.json',
        'method': 'POST',
    },

    # Blocking methods
    'createBlock': {
        'url': '/blocks/create/{{id}}.json',
        'method': 'POST',
    },
    'destroyBlock': {
        'url': '/blocks/destroy/{{id}}.json',
        'method': 'POST',
    },
    'getBlocking': {
        'url': '/blocks/blocking.json',
        'method': 'GET',
    },
    'getBlockedIDs': {
        'url': '/blocks/blocking/ids.json',
        'method': 'GET',
    },
    'checkIfBlockExists': {
        'url': '/blocks/exists.json',
        'method': 'GET',
    },

    # Trending methods
    'getCurrentTrends': {
        'url': '/trends/current.json',
        'method': 'GET',
    },
    'getDailyTrends': {
        'url': '/trends/daily.json',
        'method': 'GET',
    },
    'getWeeklyTrends': {
        'url': '/trends/weekly.json',
        'method': 'GET',
    },
    'availableTrends': {
        'url': '/trends/available.json',
        'method': 'GET',
    },
    'trendsByLocation': {
        'url': '/trends/{{woeid}}.json',
        'method': 'GET',
    },

    # Saved Searches
    'getSavedSearches': {
        'url': '/saved_searches.json',
        'method': 'GET',
    },
    'showSavedSearch': {
        'url': '/saved_searches/show/{{id}}.json',
        'method': 'GET',
    },
    'createSavedSearch': {
        'url': '/saved_searches/create.json',
        'method': 'GET',
    },
    'destroySavedSearch': {
        'url': '/saved_searches/destroy/{{id}}.json',
        'method': 'GET',
    },

    # List API methods/endpoints. Fairly exhaustive and annoying in general. ;P
    'createList': {
        'url': '/lists/create.json',
        'method': 'POST',
    },
    'updateList': {
        'url': '/lists/update.json',
        'method': 'POST',
    },
    'showLists': {
        'url': '/lists.json',
        'method': 'GET',
    },
    'getListMemberships': {
        'url': '/lists/memberships.json',
        'method': 'GET',
    },
    'getListSubscriptions': {
        'url': '/lists/subscriptions.json',
        'method': 'GET',
    },
    'isListSubscriber': {
        'url': '/lists/subscribers/show.json',
        'method': 'GET',
    },
    'deleteList': {
        'url': '/lists/destroy.json',
        'method': 'POST',
    },
    'getListTimeline': {
        'url': '/{{username}}/lists/{{list_id}}/statuses.json',
        'method': 'GET',
    },
    'getSpecificList': {
        'url': '/lists/show.json',
        'method': 'GET',
    },
    'getListStatuses': {
        'url': '/lists/statuses.json',
        'method': 'GET'
    },
    'isListMember': {
        'url': '/lists/members/show.json',
        'method': 'GET',
    },
    'addListMember': {
        'url': '/lists/members/create.json',
        'method': 'POST',
    },
    'getListMembers': {
        'url': '/lists/members.json',
        'method': 'GET',
    },
    'deleteListMember': {
        'url': '/lists/members/destroy.json',
        'method': 'POST',
    },
    'getListSubscribers': {
        'url': '/lists/subscribers.json',
        'method': 'GET',
    },
    'subscribeToList': {
        'url': '/lists/subscribers/create.json',
        'method': 'POST',
    },
    'unsubscribeFromList': {
        'url': '/lists/subscribers/destroy.json',
        'method': 'POST',
    },

    # The one-offs
    'notificationFollow': {
        'url': '/notifications/follow/follow.json',
        'method': 'POST',
    },
    'notificationLeave': {
        'url': '/notifications/leave/leave.json',
        'method': 'POST',
    },
    'updateDeliveryService': {
        'url': '/account/update_delivery_device.json',
        'method': 'POST',
    },
    'reportSpam': {
        'url': '/report_spam.json',
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
    420: ('Enhance Your Calm', 'Returned by the Search and Trends API when you are being rate limited.'),
    500: ('Internal Server Error', 'Something is broken. Please post to the group so the Twitter team can investigate.'),
    502: ('Bad Gateway', 'Twitter is down or being upgraded.'),
    503: ('Service Unavailable', 'The Twitter servers are up, but overloaded with requests. Try again later.'),
}
