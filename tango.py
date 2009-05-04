"""
    Django-Twitter (Tango) utility functions. Huzzah.
"""

import simplejson, urllib, urllib2

class tango:
    def __init__(self, twitter_user):
        # Authenticate here?
        self.twitter_user = twitter_user
    
    def getUserTimeline(self, optional_count):
        userTimelineURL = "http://twitter.com/statuses/user_timeline/" + self.twitter_user + ".json" + ("" if optional_count is None else "?count=" + optional_count)
        userTimeline = simplejson.load(urllib2.urlopen(userTimelineURL))
        formattedTimeline = []
        for tweet in userTimeline:
            formattedTimeline.append(tweet['text'])
        return formattedTimeline

    def getSearchTimeline(self, search_query, optional_page):
        params = urllib.urlencode({'q': search_query, 'rpp': optional_page}) # Doesn't hurt to do pages this way. *shrug*
        searchTimeline = simplejson.load(urllib2.urlopen("http://search.twitter.com/search.json", params))
        formattedTimeline = []
        for tweet in searchTimeline['results']:
            formattedTimeline.append(tweet['text'])
        return formattedTimeline

    def getTrendingTopics(self):
        trendingTopicsURL = "http://search.twitter.com/trends.json"
        trendingTopics = simplejson.load(urllib.urlopen(trendingTopicsURL))
        pass # for now, coming soon


