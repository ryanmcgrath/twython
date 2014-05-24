from twython import Twython, TwythonError

# Optionally accept user data from the command line (or elsewhere).
#
# Usage: block_user.py A_Twitter_Troll

import sys

if len(sys.argv) >= 2:
    target = sys.argv[1]
else:
    target = raw_input("User to follow: ")  # For Python 3.x use: target = input("User to follow: ")

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

try:
    twitter.create_block(screen_name=target, skip_status="true")
except TwythonError as e:
    print(e)
