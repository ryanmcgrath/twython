import twython.core as twython

# Instantiate Twython with Basic (HTTP) Authentication
twitter = twython.setup(username="example", password="example")
twitter.updateProfileImage("myImage.png")
