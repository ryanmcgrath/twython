import twython

# Instantiate with Basic (HTTP) Authentication
twitter = twython.setup(authtype="Basic", username="example", password="example")

# This returns the rate limit for the requesting IP
rateLimit = twitter.getRateLimitStatus()

# This returns the rate limit for the requesting authenticated user
rateLimit = twitter.getRateLimitStatus(rate_for="user")
