from twython import Twython

"""
    Note: for any method that'll require you to be authenticated (updating
    things, etc)
    you'll need to go through the OAuth authentication ritual. See the example
    Django application that's included with this package for more information.
"""
twitter = Twython()

# OAuth ritual...


twitter.updateStatus(status="See how easy this was?")
