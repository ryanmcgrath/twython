import tango

# Using no authentication and specifying Debug
twitter = tango.setup(debug=True)

# Using Basic Authentication
twitter = tango.setup(authtype="Basic", username="example", password="example")

# Using OAuth Authentication (Note: OAuth is the default, specify Basic if needed)
auth_keys = {"consumer_key": "yourconsumerkey", "consumer_secret": "yourconsumersecret"}
twitter = tango.setup(username="example", password="example", oauth_keys=auth_keys)
