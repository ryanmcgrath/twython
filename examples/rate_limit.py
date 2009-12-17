import twython.core as twython

# Instantiate with Basic (HTTP) Authentication
twitter = twython.setup(username="example", password="example")

# This returns the rate limit for the requesting IP
rateLimit = twitter.getRateLimitStatus()

# This returns the rate limit for the requesting authenticated user
rateLimit = twitter.getRateLimitStatus(rate_for="user")
