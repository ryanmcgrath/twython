Twython - Easy Twitter utilities in Python
=========================================================================================
Ah, Twitter, your API used to be so awesome, before you went and implemented the crap known
as OAuth 1.0. However, since you decided to force your entire development community over a barrel
about it, I suppose Twython has to support this. So, that said...

If you used this library and it all stopped working, it's because of the Authentication method change.
=========================================================================================================
Twitter recently disabled the use of "Basic Authentication", which is why, if you used Twython previously,
you probably started getting a ton of 401 errors. To fix this, we should note one thing...

You need to change how authentication works in your program/application. If you're using a command line
application or something, you'll probably languish in hell for a bit, because OAuth wasn't really designed
for those types of use cases. Twython cannot help you with that or fix the annoying parts of OAuth.

If you need OAuth, though, Twython now supports it, and ships with a skeleton Django application to get you started.
Enjoy!

Requirements (2.6~ and below; for 3k, read section further down)
-----------------------------------------------------------------------------------------------------
Twython (for versions of Python before 2.6) requires a library called
"simplejson". Depending on your flavor of package manager, you can do the following...

    (pip install | easy_install) simplejson

Twython also requires the (most excellent) OAuth2 library for handling OAuth tokens/signing/etc. Again...

    (pip install | easy_install) oauth2

Installation
-----------------------------------------------------------------------------------------------------
Installing Twython is fairly easy. You can...

    (pip install | easy_install) twython

...or, you can clone the repo and install it the old fashioned way.


    git clone git://github.com/ryanmcgrath/twython.git
    cd twython
    sudo python setup.py install

Example Use
-----------------------------------------------------------------------------------------------------
``` python
from twython import Twython

twitter = Twython()
results = twitter.search(q = "bert")

# More function definitions can be found by reading over twython/twitter_endpoints.py, as well
# as skimming the source file. Both are kept human-readable, and are pretty well documented or
# very self documenting.
```

Streaming API
----------------------------------------------------------------------------------------------------
Twython, as of v1.5.0, now includes an experimental **[Twitter Streaming API](https://dev.twitter.com/docs/streaming-api)** handler.
Usage is as follows; it's designed to be open-ended enough that you can adapt it to higher-level (read: Twitter must give you access)
streams. This also exists in large part (read: pretty much in full) thanks to the excellent **[python-requests](http://docs.python-requests.org/en/latest/) library by
Kenneth Reitz.

**Example Usage:**  
``` python  
import json  
from twython import Twython  

def on_results(results):  
    """  
        A callback to handle passed results. Wheeee.  
    """  
    print json.dumps(results)  

Twython.stream({  
    'username': 'your_username',  
    'password': 'your_password',  
    'track': 'python'  
}, on_results)  
```  


A note about the development of Twython (specifically, 1.3)
----------------------------------------------------------------------------------------------------
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
-----------------------------------------------------------------------------------------------------
There's an experimental version of Twython that's made for Python 3k. This is currently not guaranteed to
work in all situations, but it's provided so that others can grab it and hack on it.
If you choose to try it out, be aware of this.

**OAuth is now working thanks to updates from [Hades](https://github.com/hades). You'll need to grab
his [Python 3 branch for python-oauth2](https://github.com/hades/python-oauth2/tree/python3) to have it work, though.**

Questions, Comments, etc?
-----------------------------------------------------------------------------------------------------
My hope is that Twython is so simple that you'd never *have* to ask any questions, but if
you feel the need to contact me for this (or other) reasons, you can hit me up
at ryan@venodesigns.net.

You can also follow me on Twitter - **[@ryanmcgrath](http://twitter.com/ryanmcgrath)**.

Twython is released under an MIT License - see the LICENSE file for more information.

Want to help?
-----------------------------------------------------------------------------------------------------
Twython is useful, but ultimately only as useful as the people using it (say that ten times fast!). If you'd
like to help, write example code, contribute patches, document things on the wiki, tweet about it. Your help
is always appreciated!


Special Thanks to...
-----------------------------------------------------------------------------------------------------
This is a list of all those who have contributed code to Twython in some way, shape, or form. I think it's
exhaustive, but I could be wrong - if you think your name should be here and it's not, please contact
me and let me know (or just issue a pull request on GitHub, and leave a note about it so I can just accept it ;)).

- **[Mike Helmick (michaelhelmick)](https://github.com/michaelhelmick)**, multiple fixes and proper `requests` integration.  
- **[kracekumar](https://github.com/kracekumar)**, early `requests` work and various fixes.  
- **[Erik Scheffers (eriks5)](https://github.com/eriks5)**, various fixes regarding OAuth callback URLs.  
- **[Jordan Bouvier (jbouvier)](https://github.com/jbouvier)**, various fixes regarding OAuth callback URLs.  
- **[Dick Brouwer (dikbrouwer)](https://github.com/dikbrouwer)**, fixes for OAuth Verifier in `get_authorized_tokens`.  
- **[hades](https://github.com/hades)**, Fixes to various initial OAuth issues and updates to `Twython3k` to stay current.  
- **[Alex Sutton (alexdsutton)](https://github.com/alexsdutton/twython/)**, fix for parameter substitution regular expression (catch underscores!).  
- **[Levgen Pyvovarov (bsn)](https://github.com/bsn)**, Various argument fixes, cyrillic text support.  
- **[Mark Liu (mliu7)](https://github.com/mliu7)**, Missing parameter fix for `addListMember`.  
- **[Randall Degges (rdegges)](https://github.com/rdegges)**, PEP-8 fixes, MANIFEST.in, installer fixes.  
- **[Idris Mokhtarzada (idris)](https://github.com/idris)**, Fixes for various example code pieces.  
- **[Jonathan Elsas (jelsas)](https://github.com/jelsas)**, Fix for original Streaming API stub causing import errors.  
- **[LuqueDaniel](https://github.com/LuqueDaniel)**, Extended example code where necessary.  
- **[Mesar Hameed (mhameed)](https://github.com/mhameed)**, Commit to swap `__getattr__` trick for a more debuggable solution.  
- **[Remy DeCausemaker (decause)](https://github.com/decause)**, PEP-8 contributions.  
- **[mckellister](https://github.com/mckellister)**, Fixes to `Exception`s raised by Twython (Rate Limits, etc).  
- **[tatz_tsuchiya](http://d.hatena.ne.jp/tatz_tsuchiya/20120115/1326623451), Fix for `lambda` scoping in key injection phase.  
