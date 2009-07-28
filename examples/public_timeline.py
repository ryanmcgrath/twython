import tango

# Getting the public timeline requires no authentication, huzzah
twitter = tango.setup()
public_timeline = twitter.getPublicTimeline()

for tweet in public_timeline:
	print tweet["text"]
