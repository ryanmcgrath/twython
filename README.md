Twython
=======

```Twython``` is library providing an easy (and up-to-date) way to access Twitter data in Python

Features
--------

* Query data for:
   - User information
   - Twitter lists
   - Timelines
   - Direct Messages
   - and anything found in [the docs](https://dev.twitter.com/docs/api/1.1)
* Image Uploading!
   - **Update user status with an image**
   - Change user avatar
   - Change user background image
   - Change user banner image
* Seamless Python 3 support!

Installation
------------

    (pip install | easy_install) twython

... or, you can clone the repo and install it the old fashioned way

    git clone git://github.com/ryanmcgrath/twython.git
    cd twython
    sudo python setup.py install

Usage
-----

##### Authorization URL

```python
from twython import Twython

t = Twython(app_key, app_secret)

auth_props = t.get_authentication_tokens(callback_url='http://google.com')

oauth_token = auth_props['oauth_token']
oauth_token_secret = auth_props['oauth_token_secret']

print 'Connect to Twitter via: %s' % auth_props['auth_url']
```

Be sure you have a URL set up to handle the callback after the user has allowed your app to access their data, the callback can be used for storing their final OAuth Token and OAuth Token Secret in a database for use at a later date.

##### Handling the callback

```python
from twython import Twython

# oauth_token_secret comes from the previous step
# if needed, store that in a session variable or something.
# oauth_verifier and oauth_token from the previous call is now REQUIRED # to pass to get_authorized_tokens

# In Django, to get the oauth_verifier and oauth_token from the callback
# url querystring, you might do something like this:
# oauth_token = request.GET.get('oauth_token')
# oauth_verifier = request.GET.get('oauth_verifier')

t = Twython(app_key, app_secret,
            oauth_token, oauth_token_secret)

auth_tokens = t.get_authorized_tokens(oauth_verifier)
print auth_tokens
```

*Function definitions (i.e. get_home_timeline()) can be found by reading over twython/endpoints.py*

##### Getting a user home timeline

```python
from twython import Twython

# oauth_token and oauth_token_secret are the final tokens produced
# from the 'Handling the callback' step

t = Twython(app_key, app_secret,
            oauth_token, oauth_token_secret)

# Returns an dict of the user home timeline
print t.get_home_timeline()
```

##### Catching exceptions
> Twython offers three Exceptions currently: TwythonError, TwythonAuthError and TwythonRateLimitError

```python
from twython import Twython, TwythonAuthError

t = Twython(MY_WRONG_APP_KEY, MY_WRONG_APP_SECRET,
            BAD_OAUTH_TOKEN, BAD_OAUTH_TOKEN_SECRET)

try:
    t.verify_credentials()
except TwythonAuthError as e:
    print e
```

#### Dynamic function arguments
> Keyword arguments to functions are mapped to the functions available for each endpoint in the Twitter API docs. Doing this allows us to be incredibly flexible in querying the Twitter API, so changes to the API aren't held up from you using them by this library.

> https://dev.twitter.com/docs/api/1.1/post/statuses/update says it takes "status" amongst other arguments

```python
from twython import Twython, TwythonAuthError

t = Twython(app_key, app_secret,
            oauth_token, oauth_token_secret)

try:
    t.update_status(status='Hey guys!')
except TwythonError as e:
    print e
```

> https://dev.twitter.com/docs/api/1.1/get/search/tweets says it takes "q" and "result_type" amongst other arguments

```python
from twython import Twython, TwythonAuthError

t = Twython(app_key, app_secret,
            oauth_token, oauth_token_secret)

try:
    t.search(q='Hey guys!')
    t.search(q='Hey guys!', result_type='popular')
except TwythonError as e:
    print e
```

##### Streaming API

```python
from twython import TwythonStreamer


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        print data

    def on_error(self, status_code, data):
        print status_code, data

# Requires Authentication as of Twitter API v1.1
stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

stream.statuses.filter(track='twitter')
```

Notes
-----
Twython (as of 2.7.0) is currently in the process of ONLY supporting Twitter v1.1 endpoints and deprecating all v1 endpoints! Please see the **[Twitter v1.1 API Documentation](https://dev.twitter.com/docs/api/1.1)** to help migrate your API calls!

Questions, Comments, etc?
-------------------------
My hope is that Twython is so simple that you'd never *have* to ask any questions, but if you feel the need to contact me for this (or other) reasons, you can hit me up at ryan@venodesigns.net.

Or if I'm to busy to answer, feel free to ping mikeh@ydekproductions.com as well.

Follow us on Twitter:
* **[@ryanmcgrath](http://twitter.com/ryanmcgrath)**
* **[@mikehelmick](http://twitter.com/mikehelmick)**

Want to help?
-------------
Twython is useful, but ultimately only as useful as the people using it (say that ten times fast!). If you'd like to help, write example code, contribute patches, document things on the wiki, tweet about it. Your help is always appreciated!
