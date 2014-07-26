from twython import Twython, TwythonError

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
try:
    search_results = twitter.search(q='WebsDotCom', count=50)
except TwythonError as e:
    print e

for tweet in search_results['statuses']:
    print 'Tweet from @%s Date: %s' % (tweet['user']['screen_nam\
                                       e'].encode('utf-8'),
                                       tweet['created_at'])
    print tweet['text'].encode('utf-8'), '\n'
