from twython import Twython

# Shortening URLs requires no authentication, huzzah
shortURL = Twython.shorten_url('http://www.webs.com/')

print shortURL
