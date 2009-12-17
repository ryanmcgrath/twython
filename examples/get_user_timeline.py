import twython.core as twython

# We won't authenticate for this, but sometimes it's necessary
twitter = twython.setup()
user_timeline = twitter.getUserTimeline(screen_name="ryanmcgrath")

print user_timeline
