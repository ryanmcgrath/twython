import tango
import pprint

""" Instantiate Tango with no Authentication """
twitter = tango.setup()
trends = twitter.getCurrentTrends()["trends"]

print trends
