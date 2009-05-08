#!/usr/bin/python

"""
    Django-Twitter (Tango) utility functions. Huzzah.
"""

import simplejson, urllib, urllib2, base64

# Need to support URL shortening

class tango:
    def __init__(self, authtype = None, username = None, password = None):
        self.authtype = authtype
        self.username = username
        self.password = password
        # Forthcoming auth work below, now requires base64 shiz        
        if self.authtype == "OAuth":
            pass            
        elif self.authtype == "Basic":
            print "Basic Auth"
        else:
            pass
    
    def getUserTimeline(self, count = None, since_id = None, max_id = None, page = None):
        # Fairly close to full API support, need a few other methods.
        userTimelineURL = "http://twitter.com/statuses/user_timeline/" + self.username + ".json"
        if count is not None:
            userTimelineURL += "?count=" + count
        if since_id is not None:
            userTimelineURL += "?since_id=" + since_id
        if max_id is not None:
            userTimelineURL += "?max_id=" + max_id
        if page is not None:
            userTimelineURL += "?page=" + page
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
