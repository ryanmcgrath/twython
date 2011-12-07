from twython import Twython

"""
    You'll need to go through the OAuth ritual to be able to successfully
    use this function. See the example oauth django application included in
    this package for more information.
"""
twitter = Twython()
twitter.updateProfileImage("myImage.png")
