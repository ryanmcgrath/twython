from twython import Twython, TwythonError

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
try:
    user_timeline = twitter.get_user_timeline(screen_name='ryanmcgrath')
except TwythonError as e:
    print e

print user_timeline
