#!/usr/bin/python

"""
    Django-Twitter (Tango) utility functions. Huzzah.
"""

import urllib, urllib2

try:
    import simplejson
except:
    print "Tango requires the simplejson library to work. http://www.undefined.org/python/"

# Should really deprecate httplib2 at some point...
try:
    import httplib2
except:
    print "Tango requires httplib2 for authentication purposes. http://code.google.com/p/httplib2/"

try:
    import oauth
except:
    print "Tango requires oauth for authentication purposes. http://oauth.googlecode.com/svn/code/python/oauth/oauth.py"


# Need to support URL shortening

class setup:
    def __init__(self, authtype = "OAuth", username = None, password = None, oauth_keys = None):
        self.authtype = authtype
        self.authenticated = False
        self.username = username
        self.password = password
        self.oauth_keys = oauth_keys
        self.http = httplib2.Http() # For Basic Auth...
        if self.username is not None and self.password is not None:
            if self.authtype == "OAuth":
                pass            
            elif self.authtype == "Basic":
                self.http.add_credentials(self.username, self.password)
                self.authenticated = True
        else:
            pass
    
    def shortenURL(self, url_to_shorten):
        # Perhaps we should have fallbacks here in case the is.gd API limit gets hit? Maybe allow them to set the host?
        shortURL = urllib2.urlopen("http://is.gd/api.php?" + urllib.urlencode({"longurl": url_to_shorten})).read()
        return shortURL

    def constructApiURL(self, base_url, params):
        queryURL = base_url
        questionMarkUsed = False
        for param in params:
            if params[param] is not None:
                queryURL += (("&" if questionMarkUsed is True else "?") + param + "=" + params[param])
                questionMarkUsed = True
        return queryURL
    
    def getPublicTimeline(self):
        publicTimeline = simplejson.load(urllib2.urlopen("http://twitter.com/statuses/public_timeline.json"))
        formattedTimeline = []
        for tweet in publicTimeline:
            formattedTimeline.append(tweet['text'])
        return formattedTimeline
    
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
    
    def getUserMentions(self, **kwargs):
        if self.authenticated is True:
            if self.authtype == "Basic":
                pass
            else:
                pass
        else:
            print "getUserMentions() requires you to be authenticated."
            pass

    def updateStatus(self, status = None, in_reply_to_status_id = None):
        if self.authenticated is True:
            if self.authtype == "Basic":
                self.http.request("http://twitter.com/statuses/update.json", "POST", urllib.urlencode({"status": status}, {"in_reply_to_status_id": in_reply_to_status_id}))
            else:
                print "Sorry, OAuth support is still forthcoming. Feel free to help out on this front!"
                pass
        else:
            print "updateStatus() requires you to be authenticated."
            pass
    
    def destroyStatus(self, id):
        if self.authenticated is True:
            self.http.request("http://twitter.com/status/destroy/" + id + ".json", "POST")
        else:
            print "destroyStatus() requires you to be authenticated."
            pass
    
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
