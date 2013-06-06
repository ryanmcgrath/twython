.. _basic-usage:

Basic Usage
===========

This section will cover how to use Twython and interact with some basic Twitter API calls

Before you make any API calls, make sure you :ref:`authenticated <starting-out>` the user!

Create a Twython instance with your application keys and the users OAuth tokens::

    from twython import Twython
    twitter = Twython(APP_KEY, APP_SECRET
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

.. admonition:: Important

    All sections on this page will assume you're using a Twython instance

What Twython Returns
--------------------

Twython returns a dictionary of JSON response from Twitter

User Information
----------------

Documentation: https://dev.twitter.com/docs/api/1.1/get/account/verify_credentials

::

    twitter.verify_credentials()

Authenticated Users Home Timeline
---------------------------------

Documentation: https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline

::

    twitter.get_home_timeline()

Search
------

Documentation: https://dev.twitter.com/docs/api/1.1/get/search/tweets

::

    twitter.search(q='python')

To help explain :ref:`dynamic function arguments <starting-out>` a little more, you can see that the previous call used the keyword argument ``q``, that is because Twitter specifies in their `search documentation <https://dev.twitter.com/docs/api/1.1/get/search/tweets>`_ that the search call accepts the parameter "q". You can pass mutiple keyword arguments. The search documentation also specifies that the call accepts the parameter "result_type"

::

    twitter.search(q='python', result_type='popular')

Updating Status
---------------

Documentation: https://dev.twitter.com/docs/api/1/post/statuses/update

::

    twitter.update_status(status='See how easy using Twython is!')

