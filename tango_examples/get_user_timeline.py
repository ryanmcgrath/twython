import tango

# We won't authenticate for this, but sometimes it's necessary
twitter = tango.setup()
user_timeline = twitter.getUserTimeline(id=None, screen_name="ryanmcgrath")

print user_timeline
