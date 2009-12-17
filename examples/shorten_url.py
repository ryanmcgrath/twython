import twython as twython

# Shortening URLs requires no authentication, huzzah
twitter = twython.setup()
shortURL = twitter.shortenURL("http://www.webs.com/")

print shortURL
