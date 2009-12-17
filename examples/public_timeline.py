import twython.core as twython

# Getting the public timeline requires no authentication, huzzah
twitter = twython.setup()
public_timeline = twitter.getPublicTimeline()

for tweet in public_timeline:
	print tweet["text"]
