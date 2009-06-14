import tango, pprint

# Authenticate using Basic (HTTP) Authentication
twitter = tango.setup(authtype="Basic", username="example", password="example")
friends_timeline = twitter.getFriendsTimeline(count="150", page="3")

for tweet in friends_timeline:
	print tweet["text"]
