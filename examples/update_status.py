import twython

# Create a Twython instance using Basic (HTTP) Authentication and update our Status
twitter = twython.setup(authtype="Basic", username="example", password="example")
twitter.updateStatus("See how easy this was?")
