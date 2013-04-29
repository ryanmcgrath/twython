Twython
=======
``Twython`` is library providing an easy (and up-to-date) way to access Twitter data in Python

Features
--------

* Query data for:
   - User information
   - Twitter lists
   - Timelines
   - Direct Messages
   - and anything found in `the docs <https://dev.twitter.com/docs/api/1.1>`_
* Image Uploading!
   - **Update user status with an image**
   - Change user avatar
   - Change user background image
   - Change user banner image

Installation
------------
::

    pip install twython

... or, you can clone the repo and install it the old fashioned way

::

    git clone git://github.com/ryanmcgrath/twython.git
    cd twython
    sudo python setup.py install


Usage
-----

Authorization URL
~~~~~~~~~~~~~~~~~
::

    from twython import Twython

    t = Twython(app_key, app_secret)

    auth_props = t.get_authentication_tokens(callback_url='http://google.com')

    oauth_token = auth_props['oauth_token']
    oauth_token_secret = auth_props['oauth_token_secret']

    print 'Connect to Twitter via: %s' % auth_props['auth_url']

Be sure you have a URL set up to handle the callback after the user has allowed your app to access their data, the callback can be used for storing their final OAuth Token and OAuth Token Secret in a database for use at a later date.

Handling the callback
~~~~~~~~~~~~~~~~~~~~~
::

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

*Function definitions (i.e. getHomeTimeline()) can be found by reading over twython/endpoints.py*

Getting a user home timeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    from twython import Twython

    # oauth_token and oauth_token_secret are the final tokens produced
    # from the 'Handling the callback' step

    t = Twython(app_key, app_secret,
                oauth_token, oauth_token_secret)
    
    # Returns an dict of the user home timeline
    print t.getHomeTimeline()


Catching exceptions
~~~~~~~~~~~~~~~~~~~

    Twython offers three Exceptions currently: ``TwythonError``, ``TwythonAuthError`` and ``TwythonRateLimitError``

::

    from twython import Twython, TwythonAuthError

    t = Twython(MY_WRONG_APP_KEY, MY_WRONG_APP_SECRET,
                BAD_OAUTH_TOKEN, BAD_OAUTH_TOKEN_SECRET)

    try:
        t.verifyCredentials()
    except TwythonAuthError as e:
        print e


Streaming API
~~~~~~~~~~~~~
*Usage is as follows; it's designed to be open-ended enough that you can adapt it to higher-level (read: Twitter must give you access)
streams.*

::

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


Notes
-----
* Twython (as of 2.7.0) is currently in the process of ONLY supporting Twitter v1.1 endpoints and deprecating all v1 endpoints! Please see the `Twitter API Documentation <https://dev.twitter.com/docs/api/1.1>`_ to help migrate your API calls!

Twython && Django
-----------------
If you're using Twython with Django, there's a sample project showcasing OAuth and such **[that can be found here](https://github.com/ryanmcgrath/twython-django)**. Feel free to peruse!

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
Full compatiabilty with Python 3 is now available seamlessly in the main Twython package. The Twython 3k package has been removed as of Twython 2.8.0

Questions, Comments, etc?
-------------------------
My hope is that Twython is so simple that you'd never *have* to ask any questions, but if you feel the need to contact me for this (or other) reasons, you can hit me up at ryan@venodesigns.net.

You can also follow me on Twitter - `@ryanmcgrath <https://twitter.com/ryanmcgrath>`_

Want to help?
-------------
Twython is useful, but ultimately only as useful as the people using it (say that ten times fast!). If you'd like to help, write example code, contribute patches, document things on the wiki, tweet about it. Your help is always appreciated!
