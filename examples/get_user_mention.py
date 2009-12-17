import twython.core as twython

twitter = twython.setup(username="example", password="example")
mentions = twitter.getUserMentions(count="150")

print mentions
