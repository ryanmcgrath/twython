Twython
=======


.. image:: https://badge.fury.io/py/twython.png
        :target: http://badge.fury.io/py/twython
.. image:: https://travis-ci.org/ryanmcgrath/twython.png?branch=master
        :target: https://travis-ci.org/ryanmcgrath/twython
.. image:: https://pypip.in/d/twython/badge.png
        :target: https://crate.io/packages/twython/
.. image:: https://coveralls.io/repos/ryanmcgrath/twython/badge.png?branch=master
        :target: https://coveralls.io/r/ryanmcgrath/twython?branch=master

``Twython`` is the premier Python library providing an easy (and up-to-date) way to access Twitter data. Actively maintained and featuring support for Python 2.6+ and Python 3. It's been battle tested by companies, educational institutions and individuals alike. Try it today!

Features
--------

- Query data for:
    - User information
    - Twitter lists
    - Timelines
    - Direct Messages
    - and anything found in `the docs <https://dev.twitter.com/docs/api/1.1>`_
- Image Uploading:
    - Update user status with an image
    - Change user avatar
    - Change user background image
    - Change user banner image
- OAuth 2 Application Only (read-only) Support
- Support for Twitter's Streaming API
- Seamless Python 3 support!

Installation
------------

Install Twython via `pip <http://www.pip-installer.org/>`_

.. code-block:: bash

    $ pip install twython

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_

.. code-block:: bash

    $ easy_install twython

But, hey... `that's up to you <http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install>`_.

Or, if you want the code that is currently on GitHub

.. code-block:: bash

    git clone git://github.com/ryanmcgrath/twython.git
    cd twython
    python setup.py install

Documentation
-------------

Documentation is available at https://twython.readthedocs.org/en/latest/

Starting Out
------------

First, you'll want to head over to https://dev.twitter.com/apps and register an application!

After you register, grab your applications ``Consumer Key`` and ``Consumer Secret`` from the application details tab.

The most common type of authentication is Twitter user authentication using OAuth 1. If you're a web app planning to have users sign up with their Twitter account and interact with their timelines, updating their status, and stuff like that this **is** the authentication for you!

First, you'll want to import Twython

.. code-block:: python

    from twython import Twython

Authentication
~~~~~~~~~~~~~~

Obtain Authorization URL
^^^^^^^^^^^^^^^^^^^^^^^^

Now, you'll want to create a Twython instance with your ``Consumer Key`` and ``Consumer Secret``

    Only pass *callback_url* to *get_authentication_tokens* if your application is a Web Application

    Desktop and Mobile Applications **do not** require a callback_url

.. code-block:: python

    APP_KEY = 'YOUR_APP_KEY'
    APP_SECRET = 'YOUR_APP_SECRET'

    twitter = Twython(APP_KEY, APP_SECRET)

    auth = twitter.get_authentication_tokens(callback_url='http://mysite.com/callback')

From the ``auth`` variable, save the ``oauth_token`` and ``oauth_token_secret`` for later use (these are not the final auth tokens). In Django or other web frameworks, you might want to store it to a session variable

.. code-block:: python

    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

Send the user to the authentication url, you can obtain it by accessing

.. code-block:: python

    auth['auth_url']

Handling the Callback
^^^^^^^^^^^^^^^^^^^^^

    If your application is a Desktop or Mobile Application *oauth_verifier* will be the PIN code

After they authorize your application to access some of their account details, they'll be redirected to the callback url you specified in ``get_autentication_tokens``

You'll want to extract the ``oauth_verifier`` from the url.

Django example:

.. code-block:: python

    oauth_verifier = request.GET['oauth_verifier']

Now that you have the ``oauth_verifier`` stored to a variable, you'll want to create a new instance of Twython and grab the final user tokens

.. code-block:: python

    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    final_step = twitter.get_authorized_tokens(oauth_verifier)

Once you have the final user tokens, store them in a database for later use!::

    OAUTH_TOKEN = final_step['oauth_token']
    OAUTH_TOKEN_SECERT = final_step['oauth_token_secret']

For OAuth 2 (Application Only, read-only) authentication, see `our documentation <https://twython.readthedocs.org/en/latest/usage/starting_out.html#oauth-2-application-authentication>`_

Dynamic Function Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~

Keyword arguments to functions are mapped to the functions available for each endpoint in the Twitter API docs. Doing this allows us to be incredibly flexible in querying the Twitter API, so changes to the API aren't held up from you using them by this library.

Basic Usage
-----------

**Function definitions (i.e. get_home_timeline()) can be found by reading over twython/endpoints.py**

Create a Twython instance with your application keys and the users OAuth tokens

.. code-block:: python

    from twython import Twython
    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

Authenticated Users Home Timeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Documentation: https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline

.. code-block:: python

    twitter.get_home_timeline()

Updating Status
~~~~~~~~~~~~~~~

This method makes use of dynamic arguments, `read more about them <https://twython.readthedocs.org/en/latest/usage/starting_out.html#dynamic-function-arguments>`_

Documentation: https://dev.twitter.com/docs/api/1/post/statuses/update

.. code-block:: python

    twitter.update_status(status='See how easy using Twython is!')

Searching
~~~~~~~~~

    https://dev.twitter.com/docs/api/1.1/get/search/tweets says it takes "q" and "result_type" amongst other arguments

.. code-block:: python

    twitter.search(q='twitter')
    twitter.search(q='twitter', result_type='popular')

Advanced Usage
--------------

- `Advanced Twython Usage <https://twython.readthedocs.org/en/latest/usage/advanced_usage.html>`_
- `Streaming with Twython <https://twython.readthedocs.org/en/latest/usage/streaming_api.html>`_


Notes
-----

- Twython 3.0.0 has been injected with 1000mgs of pure awesomeness! OAuth 2 application authentication is now supported. And a *whole lot* more! See the `CHANGELOG <https://github.com/ryanmcgrath/twython/blob/master/HISTORY.rst#300-2013-06-18>`_ for more details!

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
