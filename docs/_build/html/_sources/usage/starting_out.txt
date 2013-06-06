.. _starting-out:

Starting Out
============

This section is going to help you understand creating a Twitter Application, authenticating a user, and making basic API calls

Beginning
---------

First, you'll want to head over to https://dev.twitter.com/apps and register an application!

After you register, grab your applications ``Consumer Key`` and ``Consumer Secret`` from the application details tab.

Now you're ready to start authentication!

Authentication
--------------

First, you'll want to import Twython::

    from twython import Twython

Now, you'll want to create a Twython instance with your ``Consumer Key`` and ``Consumer Secert``

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
---------------------

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

The Twython API Table
---------------------

In the Twython package is a file called ``endpoints.py`` which holds a dictionary of all Twitter API endpoints. This is so Twython's core ``api.py`` isn't cluttered with 50+ methods. We dynamically register these funtions when a Twython object is initiated.

Dynamic Function Arguments
--------------------------

Keyword arguments to functions are mapped to the functions available for each endpoint in the Twitter API docs. Doing this allows us to be incredibly flexible in querying the Twitter API, so changes to the API aren't held up from you using them by this library.

-----------------------

Now that you have your application tokens and user tokens, check out the :ref:`basic usage <basic-usage>` section.
