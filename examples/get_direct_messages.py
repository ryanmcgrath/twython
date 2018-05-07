from twython import Twython, TwythonError
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


get_list = twitter.get_direct_messages()
#Returns All Twitter DM information which is a lot in a list format

dm_dict = get_list[0]
#Sets get_list to a dictionary, the number in the list is the direct message retrieved
#That means that 0 is the most recent and n-1 is the last DM revieved.
#You can cycle through all the numbers and it will return the text and the sender id of each

print dm_dict['text']
#Gets the text from the dictionary

print dm_dict['sender']['id']
#Gets the ID of the sender
