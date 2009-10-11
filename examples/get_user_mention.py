import twitter

twitter = twython.setup(authtype="Basic", username="example", password="example")
mentions = twitter.getUserMentions(count="150")

print mentions
