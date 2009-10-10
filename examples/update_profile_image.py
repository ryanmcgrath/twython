import twython

# Instantiate Twython with Basic (HTTP) Authentication
twitter = twython.setup(authtype="Basic", username="example", password="example")
twitter.updateProfileImage("myImage.png")
