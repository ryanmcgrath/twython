Twython
=======

.. image:: https://travis-ci.org/ryanmcgrath/twython.png?branch=master
        :target: https://travis-ci.org/ryanmcgrath/twython
.. image:: https://pypip.in/d/twython/badge.png
        :target: https://crate.io/packages/twython/

``Twython`` is a library providing an easy (and up-to-date) way to access Twitter data in Python. Actively maintained and featuring support for both Python 2.6+ and Python 3, it's been battle tested by companies, educational institutions and individuals alike. Try it today!

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
* Support for Twitter's Streaming API
* Seamless Python 3 support!

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

*Function definitions (i.e. get_home_timeline()) can be found by reading over twython/endpoints.py*

Getting a user home timeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    from twython import Twython

    # oauth_token and oauth_token_secret are the final tokens produced
    # from the 'Handling the callback' step

    t = Twython(app_key, app_secret,
                oauth_token, oauth_token_secret)
    
    # Returns an dict of the user home timeline
    print t.get_home_timeline()


Catching exceptions
~~~~~~~~~~~~~~~~~~~

    Twython offers three Exceptions currently: ``TwythonError``, ``TwythonAuthError`` and ``TwythonRateLimitError``

::

    from twython import Twython, TwythonAuthError

    t = Twython(MY_WRONG_APP_KEY, MY_WRONG_APP_SECRET,
                BAD_OAUTH_TOKEN, BAD_OAUTH_TOKEN_SECRET)

    try:
        t.verify_credentials()
    except TwythonAuthError as e:
        print e

Dynamic function arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~
    Keyword arguments to functions are mapped to the functions available for each endpoint in the Twitter API docs. Doing this allows us to be incredibly flexible in querying the Twitter API, so changes to the API aren't held up from you using them by this library.

    https://dev.twitter.com/docs/api/1.1/post/statuses/update says it takes "status" amongst other arguments

::

    from twython import Twython, TwythonAuthError

    t = Twython(app_key, app_secret,
                oauth_token, oauth_token_secret)

    try:
        t.update_status(status='Hey guys!')
    except TwythonError as e:
        print e

and
    https://dev.twitter.com/docs/api/1.1/get/search/tweets says it takes "q" and "result_type" amongst other arguments

::

    from twython import Twython, TwythonAuthError

    t = Twython(app_key, app_secret,
                oauth_token, oauth_token_secret)

    try:
        t.search(q='Hey guys!')
        t.search(q='Hey guys!', result_type='popular')
    except TwythonError as e:
        print e

Posting a Status with an Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    from twython import Twython

    t = Twython(app_key, app_secret,
                oauth_token, oauth_token_secret)

    # The file key that Twitter expects for updating a status with an image
    # is 'media', so 'media' will be apart of the params dict.

    # You can pass any object that has a read() function (like a StringIO object)
    # In case you wanted to resize it first or something!

    photo = open('/path/to/file/image.jpg', 'rb')
    t.update_status_with_media(media=photo, status='Check out my image!')

Posting a Status with an Editing Image  *(This example resizes an image)*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    from twython import Twython

    t = Twython(app_key, app_secret,
                oauth_token, oauth_token_secret)

    # Like I said in the previous section, you can pass any object that has a
    # read() method

    # Assume you are working with a JPEG

    from PIL import Image
    from StringIO import StringIO

    photo = Image.open('/path/to/file/image.jpg')

    basewidth = 320
    wpercent = (basewidth / float(photo.size[0]))
    height = int((float(photo.size[1]) * float(wpercent)))
    photo = photo.resize((basewidth, height), Image.ANTIALIAS)

    image_io = StringIO.StringIO()
    photo.save(image_io, format='JPEG')

    # If you do not seek(0), the image will be at the end of the file and
    # unable to be read
    image_io.seek(0)

    t.update_status_with_media(media=photo, status='Check out my edited image!')

Streaming API
~~~~~~~~~~~~~

::

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


Notes
-----
* Twython (as of 2.7.0) now supports ONLY Twitter v1.1 endpoints! Please see the **[Twitter v1.1 API Documentation](https://dev.twitter.com/docs/api/1.1)** to help migrate your API calls!
* As of Twython 2.9.1, all method names conform to PEP8 standards. For backwards compatibility, we internally check and catch any calls made using the old (pre 2.9.1) camelCase method syntax. We will continue to support this for the foreseeable future for all old methods (raising a DeprecationWarning where appropriate), but you should update your code if you have the time.

Questions, Comments, etc?
-------------------------
My hope is that Twython is so simple that you'd never *have* to ask any questions, but if you feel the need to contact me for this (or other) reasons, you can hit me up at ryan@venodesigns.net.

Or if I'm to busy to answer, feel free to ping mikeh@ydekproductions.com as well.

Follow us on Twitter:

- `@ryanmcgrath <https://twitter.com/ryanmcgrath>`_
- `@mikehelmick <https://twitter.com/mikehelmick>`_

Want to help?
-------------
Twython is useful, but ultimately only as useful as the people using it (say that ten times fast!). If you'd like to help, write example code, contribute patches, document things on the wiki, tweet about it. Your help is always appreciated!
