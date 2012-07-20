from twython import Twython

""" Instantiate Twython with no Authentication """
twitter = Twython()

# twitter has now depreciated the API endpoint att getCurrentTrends()
# instead use the trendsByLocation() method - see https://dev.twitter.com/docs/api/1/get/trends/current

trends = twitter.trendsByLocation()

print trends
