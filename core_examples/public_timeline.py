from twython import Twython

# Getting the public timeline requires no authentication, huzzah
twitter = Twython()
public_timeline = twitter.getPublicTimeline()

for tweet in public_timeline:
	print tweet["text"]
