import twython.core as twython

# Using no authentication
twitter = twython.setup()

# Using Basic Authentication (core is all about basic auth, look to twython.oauth in the future for oauth)
twitter = twython.setup(username="example", password="example")
