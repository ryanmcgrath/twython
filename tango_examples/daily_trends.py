import tango

""" Instantiate Tango with no Authentication """
twitter = tango.setup()
trends = twitter.getDailyTrends()

print trends
