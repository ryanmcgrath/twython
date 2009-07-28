import tango

# Instantiate Tango with Basic (HTTP) Authentication
twitter = tango.setup(authtype="Basic", username="example", password="example")
twitter.updateProfileImage("myImage.png")
