from twython import Twython, TwythonError

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

try:
    twitter.updateStatus(status='See how easy this was?')
except TwythonError as e:
    print e
