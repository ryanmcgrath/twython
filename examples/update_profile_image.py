from twython import Twython

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

avatar = open('myImage.png', 'rb')
twitter.update_profile_image(image=avatar)
