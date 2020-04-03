from twython import Twython, TwythonError
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

get_list = twitter.get_direct_messages()
print(get_list)
