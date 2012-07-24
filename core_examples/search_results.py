from twython import Twython

""" Instantiate Twython with no Authentication """
twitter = Twython()
search_results = twitter.search(q="WebsDotCom", rpp="50")

for tweet in search_results["results"]:
    print "Tweet from @%s Date: %s" % (tweet['from_user'].encode('utf-8'),tweet['created_at'])
    print tweet['text'].encode('utf-8'),"\n"