from twython import Twython, TwythonError

# Optionally accept user data from the command line (or elsewhere).
#
# Usage:  show_status.py 463604849372704768

import sys

if len(sys.argv) >= 2:
    target = sys.argv[1]
else:
    target = raw_input("ID number of tweet to fetch: ")  # For Python 3.x use: target = input("ID number of tweet to fetch: ")

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

try:
    tweet = twitter.show_status(id=twid)
    print(tweet["user"]["name"]+" ("+tweet["user"]["screen_name"]+"): "+tweet["text"])
except TwythonError as e:
    print(e)

# This will print:  Name (screen name): the content of the tweet selected.
