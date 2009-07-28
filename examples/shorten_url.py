import tango

# Shortening URLs requires no authentication, huzzah
twitter = tango.setup()
shortURL = twitter.shortenURL("http://www.webs.com/")

print shortURL
