import twitter

""" Instantiate Twython with no Authentication """
twitter = twython.setup()
trends = twitter.getCurrentTrends()

print trends
