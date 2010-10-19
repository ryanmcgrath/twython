from twython import Twython

# We won't authenticate for this, but sometimes it's necessary
twitter = Twython()
user_timeline = twitter.getUserTimeline(screen_name="ryanmcgrath")

print user_timeline
