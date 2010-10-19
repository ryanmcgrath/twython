from twython import Twython

# Shortening URLs requires no authentication, huzzah
shortURL = Twython.shortenURL("http://www.webs.com/")

print shortURL
