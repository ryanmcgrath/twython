.. _basic-usage:

Basic Usage
===========

This section will cover how to use Twython and interact with some basic Twitter API calls

Before you make any API calls, make sure you :ref:`authenticated the user <oauth1>` (or :ref:`app <oauth2>`)!

.. note:: All sections on this page will assume you're using a Twython instance

*******************************************************************************

Authenticated Calls
-------------------

OAuth 1
~~~~~~~

Create a Twython instance with your application keys and the users OAuth tokens

.. code-block:: python

    from twython import Twython
    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

User Information
^^^^^^^^^^^^^^^^

Documentation: https://dev.twitter.com/docs/api/1.1/get/account/verify_credentials

.. code-block:: python

    twitter.verify_credentials()

Authenticated Users Home Timeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Documentation: https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline

.. code-block:: python

    twitter.get_home_timeline()

Updating Status
^^^^^^^^^^^^^^^

This method makes use of dynamic arguments, :ref:`read more about them <dynamicargexplaination>`

Documentation: https://dev.twitter.com/docs/api/1.1/post/statuses/update

.. code-block:: python

    twitter.update_status(status='See how easy using Twython is!')


OAuth 2
~~~~~~~

Create a Twython instance with your application key and access token

.. code-block:: python

    from twython import Twython
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

.. _howtosearch:

Searching
---------

.. note:: Searching can be done whether you're authenticated via OAuth 1 or OAuth 2

Documentation: https://dev.twitter.com/docs/api/1.1/get/search/tweets

.. code-block:: python

    twitter.search(q='python')

.. _dynamicargexplaination:

.. important:: To help explain :ref:`dynamic function arguments <dynamicfunctionarguments>` a little more, you can see that the previous call used the keyword argument ``q``, that is because Twitter specifies in their `search documentation <https://dev.twitter.com/docs/api/1.1/get/search/tweets>`_ that the search call accepts the parameter "q". You can pass mutiple keyword arguments. The search documentation also specifies that the call accepts the parameter "result_type"

.. code-block:: python

    twitter.search(q='python', result_type='popular')

*******************************************************************************

So, now, you're pretty well versed on making authenticated calls to Twitter using Twython. Check out the :ref:`advanced usage <advanced-usage>` section, for some functions that may be a little more complicated.
