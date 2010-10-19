from twython import Twython

""" Instantiate Twython with no Authentication """
twitter = Twython()
trends = twitter.getDailyTrends()

print trends
