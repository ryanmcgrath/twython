import twython.core as twython

# Create a Twython instance using Basic (HTTP) Authentication and update our Status
twitter = twython.setup(username="example", password="example")
twitter.updateStatus("See how easy this was?")
