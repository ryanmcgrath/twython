import twython.core as twython

""" Instantiate Twython with no Authentication """
twitter = twython.setup()
trends = twitter.getWeeklyTrends()

print trends
