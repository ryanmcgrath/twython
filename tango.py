#!/usr/bin/python

"""
    Django-Twitter (Tango) utility functions. Huzzah.
"""

import simplejson, urllib, urllib2, base64

# Need to support URL shortening

class setup:
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
    
    def constructApiURL(self, base_url, params):
        queryURL = base_url
        questionMarkUsed = False
        for param in params:
            if params[param] is not None:
                queryURL += (("&" if questionMarkUsed is True else "?") + param + "=" + params[param])
                questionMarkUsed = True
        return queryURL
    
    def getUserTimeline(self, **kwargs): 
        # 99% API compliant, I think - need to figure out Gzip compression and auto-getting based on authentication
        # By doing this with kwargs and constructing a url outside, we can stay somewhat agnostic of API changes - it's all
        # based on what the user decides to pass. We just handle the heavy lifting! :D
        userTimelineURL = self.constructApiURL("http://twitter.com/statuses/user_timeline/" + self.username + ".json", kwargs)
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
