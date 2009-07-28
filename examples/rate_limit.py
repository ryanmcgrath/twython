import tango

# Instantiate with Basic (HTTP) Authentication
twitter = tango.setup(authtype="Basic", username="example", password="example")

# This returns the rate limit for the requesting IP
rateLimit = twitter.getRateLimitStatus()

# This returns the rate limit for the requesting authenticated user
rateLimit = twitter.getRateLimitStatus(rate_for="user")
