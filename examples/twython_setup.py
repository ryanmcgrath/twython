import twython

# Using no authentication and specifying Debug
twitter = twython.setup(debug=True)

# Using Basic Authentication
twitter = twython.setup(authtype="Basic", username="example", password="example")

# Using OAuth Authentication (Note: OAuth is the default, specify Basic if needed)
auth_keys = {"consumer_key": "yourconsumerkey", "consumer_secret": "yourconsumersecret"}
twitter = twython.setup(username="example", password="example", oauth_keys=auth_keys)
