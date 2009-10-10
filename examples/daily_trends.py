import twitter

""" Instantiate Twython with no Authentication """
twitter = twitter.setup()
trends = twitter.getDailyTrends()

print trends
