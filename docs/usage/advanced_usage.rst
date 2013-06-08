.. _advanced-usage:

Advanced Usage
==============

This section will cover how to use Twython and interact with some a little more advanced API calls

Before you make any API calls, make sure you :ref:`authenticated <starting-out>` the user!

.. note:: All sections on this page will assume you're using a Twython instance

*******************************************************************************

Create a Twython instance with your application keys and the users OAuth tokens::

    from twython import Twython
    twitter = Twython(APP_KEY, APP_SECRET
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

Updating Status with Image
--------------------------

Documentation: https://dev.twitter.com/docs/api/1.1/get/account/verify_credentials

::

    photo = open('/path/to/file/image.jpg', 'rb')
    twitter.update_status_with_media(status='Checkout this cool image!', media=photo)

So now you can authenticate, update your status (with or without an image), search Twitter, and a few other things! Good luck!