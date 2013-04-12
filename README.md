Twython
=======

```Twython``` is library providing an easy (and up-to-date) way to access Twitter data in Python

Features
--------

* Query data for:
   - User information
   - Twitter lists
   - Timelines
   - User avatar URL
   - and anything found in [the docs](https://dev.twitter.com/docs/api/1.1)
* Image Uploading!
   - **Update user status with an image**
   - Change user avatar
   - Change user background image

Installation
------------

    (pip install | easy_install) twython

... or, you can clone the repo and install it the old fashioned way

    git clone git://github.com/ryanmcgrath/twython.git
    cd twython
    sudo python setup.py install

Usage
-----

###### Authorization URL

```python
from twython import Twython

t = Twython(app_key=app_key,
            app_secret=app_secret,
            callback_url='http://google.com/')

auth_props = t.get_authentication_tokens()

oauth_token = auth_props['oauth_token']
oauth_token_secret = auth_props['oauth_token_secret']

print 'Connect to Twitter via: %s' % auth_props['auth_url']
```

Be sure you have a URL set up to handle the callback after the user has allowed your app to access their data, the callback can be used for storing their final OAuth Token and OAuth Token Secret in a database for use at a later date.

###### Handling the callback

```python
from twython import Twython

'''
oauth_token and oauth_token_secret come from the previous step
if needed, store those in a session variable or something. oauth_verifier from the previous call is now required to pass to get_authorized_tokens
'''

t = Twython(app_key=app_key,
            app_secret=app_secret,
            oauth_token=oauth_token,
            oauth_token_secret=oauth_token_secret)

auth_tokens = t.get_authorized_tokens(oauth_verifier)
print auth_tokens
```

*Function definitions (i.e. getHomeTimeline()) can be found by reading over twython/twitter_endpoints.py*

###### Getting a user home timeline

```python
from twython import Twython

'''
oauth_token and oauth_token_secret are the final tokens produced
from the `Handling the callback` step
'''

t = Twython(app_key=app_key,
            app_secret=app_secret,
            oauth_token=oauth_token,
            oauth_token_secret=oauth_token_secret)

# Returns an dict of the user home timeline
print t.getHomeTimeline()
```

###### Streaming API
*Usage is as follows; it's designed to be open-ended enough that you can adapt it to higher-level (read: Twitter must give you access)
streams.*

```python
from twython import Twython

def on_results(results):
    """A callback to handle passed results. Wheeee.
    """

    print results

Twython.stream({
    'username': 'your_username',
    'password': 'your_password',
    'track': 'python'
}, on_results)
```

Notes
-----
Twython (as of 2.7.0) is currently in the process of ONLY supporting Twitter v1.1 endpoints and deprecating all v1 endpoints! Please see the **[Twitter v1.1 API Documentation](https://dev.twitter.com/docs/api/1.1)** to help migrate your API calls!

Development of Twython (specifically, 1.3)
------------------------------------------
As of version 1.3, Twython has been extensively overhauled. Most API endpoint definitions are stored
in a separate Python file, and the class itself catches calls to methods that match up in said table.

Certain functions require a bit more legwork, and get to stay in the main file, but for the most part
it's all abstracted out.

As of Twython 1.3, the syntax has changed a bit as well. Instead of Twython.core, there's a main
Twython class to import and use. If you need to catch exceptions, import those from twython as well.

Arguments to functions are now exact keyword matches for the Twitter API documentation - that means that
whatever query parameter arguments you read on Twitter's documentation (http://dev.twitter.com/doc) gets mapped
as a named argument to any Twitter function.

For example: the search API looks for arguments under the name "q", so you pass q="query_here" to search().

Doing this allows us to be incredibly flexible in querying the Twitter API, so changes to the API aren't held up
from you using them by this library.

Twython 3k
----------
There's an experimental version of Twython that's made for Python 3k. This is currently not guaranteed to
work in all situations, but it's provided so that others can grab it and hack on it.
If you choose to try it out, be aware of this.

**OAuth is now working thanks to updates from [Hades](https://github.com/hades). You'll need to grab
his [Python 3 branch for python-oauth2](https://github.com/hades/python-oauth2/tree/python3) to have it work, though.**

Questions, Comments, etc?
-------------------------
My hope is that Twython is so simple that you'd never *have* to ask any questions, but if you feel the need to contact me for this (or other) reasons, you can hit me up
at ryan@venodesigns.net.

You can also follow me on Twitter - **[@ryanmcgrath](http://twitter.com/ryanmcgrath)**.

Twython is released under an MIT License - see the LICENSE file for more information.

Want to help?
-------------
Twython is useful, but ultimately only as useful as the people using it (say that ten times fast!). If you'd like to help, write example code, contribute patches, document things on the wiki, tweet about it. Your help is always appreciated!
