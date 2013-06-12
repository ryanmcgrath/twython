.. _starting-out:

Starting Out
============

This section is going to help you understand creating a Twitter Application, authenticating a user, and making basic API calls

*******************************************************************************

Beginning
---------

First, you'll want to head over to https://dev.twitter.com/apps and register an application!

After you register, grab your applications ``Consumer Key`` and ``Consumer Secret`` from the application details tab.

Now you're ready to start authentication!

Authentication
--------------

Twython offers support for both OAuth 1 and OAuth 2 authentication.

The difference:

- :ref:`OAuth 1 <oauth1>` is for user authenticated calls (tweeting, following people, sneding DMs, etc.)
- :ref:`OAuth 2 <oauth2>` is for application authenticated calls (when you don't want to authenticate a user and make read-only calls to Twitter, i.e. searching, reading a public users timeline)

.. _oauth1:

OAuth 1 (User Authentication)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important:: Again, if your web app is planning on using interacting with users, this **IS** the authentication type for you. If you're not interested in authenticating a user and plan on making read-only calls, check out the :ref:`OAuth 2 <oauth2>` section.

First, you'll want to import Twython::

    from twython import Twython

Now, you'll want to create a Twython instance with your ``Consumer Key`` and ``Consumer Secret``

Obtain Authorization URL
^^^^^^^^^^^^^^^^^^^^^^^^

::

    APP_KEY = 'YOUR_APP_KEY'
    APP_SECET = 'YOUR_APP_SECRET'

    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens(callback_url='http://mysite.com/callback')

From the ``auth`` variable, save the ``oauth_token_secret`` for later use. In Django or other web frameworks, you might want to store it to a session variable::

    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

Send the user to the authentication url, you can obtain it by accessing::

    auth['auth_url']

Handling the Callback
^^^^^^^^^^^^^^^^^^^^^

After they authorize your application to access some of their account details, they'll be redirected to the callback url you specified in ``get_autentication_tokens``

You'll want to extract the ``oauth_token`` and ``oauth_verifier`` from the url.

Django example:
::

    OAUTH_TOKEN = request.GET['oauth_token']
    oauth_verifier = request.GET['oauth_verifier']

Now that you have the ``oauth_token`` and ``oauth_verifier`` stored to variables, you'll want to create a new instance of Twython and grab the final user tokens::

    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    final_step = twitter.get_authorized_tokens(oauth_verifier)

Once you have the final user tokens, store them in a database for later use!::

    OAUTH_TOKEN = final_step['oauth_token']
    OAUTH_TOKEN_SECERT = final_step['oauth_token_secret']

.. _oauth2:

OAuth 2 (Application Authentication)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. attention:: Just a reminder, this authentication type is for when you don't want to authenticate and interact with users and make read-only calls to Twitter

OAuth 2 authentication is 100x easier than OAuth 1.
Let's say you *just* made your application and have your ``Consumer Key`` and ``Consumer Secret``

First, you'll want to import Twython::

    from twython import Twython

Obtain an OAuth 2 Access Token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    APP_KEY = 'YOUR_APP_KEY'
    APP_SECET = 'YOUR_APP_SECRET'

    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()

    # Save ACCESS_TOKEN in a database or something for later use!

Use the Access Token
^^^^^^^^^^^^^^^^^^^^

::

    APP_KEY = 'YOUR_APP_KEY'
    ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

Now that you have your OAuth 2 access_token, maybe you'll want to perform a :ref:`search <howtosearch>` or something

The Twython API Table
---------------------

The Twython package contains a file ``endpoints.py`` which holds a Mixin of all Twitter API endpoints. This is so Twython's core ``api.py`` isn't cluttered with 50+ methods.

.. _dynamicfunctionarguments:

Dynamic Function Arguments
--------------------------

Keyword arguments to functions are mapped to the functions available for each endpoint in the Twitter API docs. Doing this allows us to be incredibly flexible in querying the Twitter API, so changes to the API aren't held up from you using them by this library.

What Twython Returns
--------------------

Twython returns native Python objects. We convert the JSON sent to us from Twitter to an object so you don't have to.


*******************************************************************************

Now that you have a little idea of the type of data you'll be receiving, briefed on how arguments are handled, and your application tokens and user oauth tokens (or access token if you're using OAuth 2), check out the :ref:`basic usage <basic-usage>` section.
