Twython
=======
``Twython`` is library providing an easy (and up-to-date) way to access Twitter data in Python

Features
--------

* Query data for:
   - User information
   - Twitter lists
   - Timelines
   - User avatar URL
   - and anything found in `the docs <https://dev.twitter.com/docs/api>`_
* Image Uploading!
   - **Update user status with an image**
   - Change user avatar
   - Change user background image

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
    
    t = Twython(app_key=app_key,
                app_secret=app_secret,
                callback_url='http://google.com/')

    auth_props = t.get_authentication_tokens()

    oauth_token = auth_props['oauth_token']
    oauth_token_secret = auth_props['oauth_token_secret']

    print 'Connect to Twitter via: %s' % auth_props['auth_url']

Be sure you have a URL set up to handle the callback after the user has allowed your app to access their data, the callback can be used for storing their final OAuth Token and OAuth Token Secret in a database for use at a later date.

Handling the callback
~~~~~~~~~~~~~~~~~~~~~
::

    '''
    oauth_token and oauth_token_secret come from the previous step
    if needed, store those in a session variable or something
    '''
    from twython import Twython

    t = Twython(app_key=app_key,
                app_secret=app_secret,
                oauth_token=oauth_token,
                oauth_token_secret=oauth_token_secret)

    auth_tokens = t.get_authorized_tokens()
    print auth_tokens

*Function definitions (i.e. getHomeTimeline()) can be found by reading over twython/twitter_endpoints.py*

Getting a user home timeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    '''
    oauth_token and oauth_token_secret are the final tokens produced
    from the `Handling the callback` step
    '''
    from twython import Twython
    
    t = Twython(app_key=app_key,
                app_secret=app_secret,
                oauth_token=oauth_token,
                oauth_token_secret=oauth_token_secret)
    
    # Returns an dict of the user home timeline
    print t.getHomeTimeline()

Get a user avatar url *(no authentication needed)*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::
    
    from twython import Twython
    
    t = Twython()
    print t.getProfileImageUrl('ryanmcgrath', size='bigger')
    print t.getProfileImageUrl('mikehelmick')

Search Twitter *(no authentication needed)*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::
    
    from twython import Twython
    t = Twython()
    print t.search(q='python')

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
* As of Twython 2.0.0, we have changed routes for functions to abide by the `Twitter Spring 2012 clean up <https://dev.twitter.com/docs/deprecations/spring-2012>`_ Please make changes to your code accordingly.


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
There's an experimental version of Twython that's made for Python 3k. This is currently not guaranteed to
work in all situations, but it's provided so that others can grab it and hack on it.
If you choose to try it out, be aware of this.

**OAuth is now working thanks to updates from [Hades](https://github.com/hades). You'll need to grab
his [Python 3 branch for python-oauth2](https://github.com/hades/python-oauth2/tree/python3) to have it work, though.**

Questions, Comments, etc?
-------------------------
My hope is that Twython is so simple that you'd never *have* to ask any questions, but if you feel the need to contact me for this (or other) reasons, you can hit me up at ryan@venodesigns.net.

You can also follow me on Twitter - `@ryanmcgrath <https://twitter.com/ryanmcgrath>`_

*Twython is released under an MIT License - see the LICENSE file for more information.*

Want to help?
-------------
Twython is useful, but ultimately only as useful as the people using it (say that ten times fast!). If you'd like to help, write example code, contribute patches, document things on the wiki, tweet about it. Your help is always appreciated!


Special Thanks to...
--------------------
This is a list of all those who have contributed code to Twython in some way, shape, or form. I think it's
exhaustive, but I could be wrong - if you think your name should be here and it's not, please contact
me and let me know (or just issue a pull request on GitHub, and leave a note about it so I can just accept it ;)).

- `Mike Helmick (michaelhelmick) <https://github.com/michaelhelmick>`_, multiple fixes and proper ``requests`` integration. Too much to list here.  
- `kracekumar <https://github.com/kracekumar>`_, early ``requests`` work and various fixes.  
- `Erik Scheffers (eriks5) <https://github.com/eriks5>`_, various fixes regarding OAuth callback URLs.
- `Jordan Bouvier (jbouvier) <https://github.com/jbouvier>`_, various fixes regarding OAuth callback URLs.
- `Dick Brouwer (dikbrouwer) <https://github.com/dikbrouwer>`_, fixes for OAuth Verifier in ``get_authorized_tokens``.
- `hades <https://github.com/hades>`_, Fixes to various initial OAuth issues and updates to ``Twython3k`` to stay current.
- `Alex Sutton (alexdsutton) <https://github.com/alexsdutton/twython/>`_, fix for parameter substitution regular expression (catch underscores!).
- `Levgen Pyvovarov (bsn) <https://github.com/bsn>`_, Various argument fixes, cyrillic text support.
- `Mark Liu (mliu7) <https://github.com/mliu7>`_, Missing parameter fix for ``addListMember``.
- `Randall Degges (rdegges) <https://github.com/rdegge>`_, PEP-8 fixes, MANIFEST.in, installer fixes.
- `Idris Mokhtarzada (idris) <https://github.com/idris>`_, Fixes for various example code pieces.
- `Jonathan Elsas (jelsas) <https://github.com/jelsas>`_, Fix for original Streaming API stub causing import errors.
- `LuqueDaniel <https://github.com/LuqueDaniel>`_, Extended example code where necessary.
- `Mesar Hameed (mhameed) <https://github.com/mhameed>`_, Commit to swap ``__getattr__`` trick for a more debuggable solution.
- `Remy DeCausemaker (decause) <https://github.com/decause>`_, PEP-8 contributions.
- `[mckellister](https://github.com/mckellister) <https://dev.twitter.com/docs/deprecations/spring-2012>`_, Fixes to ``Exception`` raised by Twython (Rate Limits, etc).
- `tatz_tsuchiya <http://d.hatena.ne.jp/tatz_tsuchiya/20120115/1326623451>`_, Fix for ``lambda`` scoping in key injection phase.
- `Voulnet (Mohammed ALDOUB) <https://github.com/Voulnet>`_, Fixes for ``http/https`` access endpoints.  
- `fumieval <https://github.com/fumieval>`_, Re-added Proxy support for 2.3.0.  
- `terrycojones <https://github.com/terrycojones>`_, Error cleanup and Exception processing in 2.3.0.  
- `Leandro Ferreira <https://github.com/leandroferreira>`_, Fix for double-encoding of search queries in 2.3.0.  
- `Chris Brown <https://github.com/chbrown>`_, Updated to use v1.1 endpoints over v1  
