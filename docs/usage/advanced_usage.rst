.. _advanced-usage:

Advanced Usage
==============

This section will cover how to use Twython and interact with some more advanced API calls

Before you make any API calls, make sure you :ref:`authenticated the user <starting-out>` (or :ref:`app <oauth2>`)!

.. note:: All sections on this page will assume you're using a Twython instance

*******************************************************************************

Create a Twython instance with your application keys and the users OAuth tokens

.. code-block:: python

    from twython import Twython
    twitter = Twython(APP_KEY, APP_SECRET
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

Updating Status with Image
--------------------------

Documentation: https://dev.twitter.com/docs/api/1.1/get/account/verify_credentials

.. code-block:: python

    photo = open('/path/to/file/image.jpg', 'rb')
    twitter.update_status_with_media(status='Checkout this cool image!', media=photo)

Posting a Status with an Editing Image
--------------------------------------

    This example resizes an image

.. code-block:: python

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

    twitter.update_status_with_media(media=photo, status='Check out my edited image!')


Search Generator
----------------

So, if you're pretty into Python, you probably know about `generators <http://docs.python.org/2/tutorial/classes.html#generators>`_

That being said, Twython offers a generator for search results and can be accessed by using the following code:

.. code-block:: python

    search = twitter.search_gen('python')
    for result in search:
        print result

Manipulate the Request (headers, proxies, etc.)
-----------------------------------------------

There are times when you may want to turn SSL verification off, send custom headers, or add proxies for the request to go through.

Twython uses the `requests <http://python-requests.org>`_ library to make API calls to Twitter. ``requests`` accepts a few parameters to allow developers to manipulate the acutal HTTP request.

Here is an example of sending custom headers to a Twitter API request:

.. code-block:: python

    from twython import Twython

    client_args = {
        'headers': {
            'User-Agent': 'My App Name'
        }
    }

    twitter = Twython(APP_KEY, APP_SECRET
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET
                      client_args=client_args)

Here is an example of sending the request through proxies:

.. code-block:: python

    from twython import Twython

    client_args = {
        'proxies': {
            'http': '10.0.10.1:8000',
            'https': '10.0.10.1:8001',
        }
    }

    twitter = Twython(APP_KEY, APP_SECRET
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET
                      client_args=client_args)

or both (and set a timeout variable):

.. code-block:: python

    from twython import Twython

    client_args = {
        'headers': {
            'User-Agent': 'My App Name'
        },
        'proxies': {
            'http': '10.0.10.1:8000',
            'https': '10.0.10.1:8001',
        }
        'timeout': 300,
    }

    twitter = Twython(APP_KEY, APP_SECRET
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET
                      client_args=client_args)

Access Headers of Previous Call
-------------------------------

There are times when you may want to check headers from the previous call.
If you wish to access headers (ex. x-rate-limit-remaining, x-rate-limit-reset, content-type), you'll use the ``get_lastfunction_header`` method.

.. code-block:: python

    from twython import Twython

    twitter = Twython(APP_KEY, APP_SECRET
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    twitter.get_home_timeline()
    twitter.get_lastfunction_header('x-rate-limit-remaining')


So now you can authenticate, update your status (with or without an image), search Twitter, and a few other things! Good luck!