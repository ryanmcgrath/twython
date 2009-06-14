import tango

# Create a Tango instance using Basic (HTTP) Authentication and update our Status
twitter = tango.setup(authtype="Basic", username="example", password="example")
twitter.updateStatus("See how easy this was?")
