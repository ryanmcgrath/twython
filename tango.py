"""
    Django-Twitter (Tango) utility functions. Huzzah.
"""

import simplejson, urllib, urllib2

class tango:
    def __init__(self, twitter_user):
        # Authenticate here?
        self.twitter_user = twitter_user
    
    def getUserTimeline(self, **kwargs):
        # Needs full API support, when I'm not so damn tired.
        userTimelineURL = "http://twitter.com/statuses/user_timeline/" + self.twitter_user + ".json"
        if kwargs["count"] is not None:
            userTimelineURL += "?count=" + kwargs["count"]
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

    def getCurrentTrends(self):
        # Returns an array of dictionary items containing the current trends
        trendingTopicsURL = "http://search.twitter.com/trends.json"
        trendingTopics = simplejson.load(urllib.urlopen(trendingTopicsURL))
        trendingTopicsArray = []
        for topic in trendingTopics['trends']:
            trendingTopicsArray.append({"name" : topic['name'], "url" : topic['url']})
        return trendingTopicsArray
