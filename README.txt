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

Requirements
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
    from twython import Twython

    twitter = Twython()
    results = twitter.searchTwitter(q="bert")

    # More function definitions can be found by reading over twython/twitter_endpoints.py, as well
    # as skimming the source file. Both are kept human-readable, and are pretty well documented or
    # very self documenting.

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

For example: the search API looks for arguments under the name "q", so you pass q="query_here" to searchTwitter().

Doing this allows us to be incredibly flexible in querying the Twitter API, so changes to the API aren't held up
from you using them by this library.

Twython 3k
-----------------------------------------------------------------------------------------------------
There's an experimental version of Twython that's made for Python 3k. This is currently not guaranteed
to work (especially with regards to OAuth), but it's provided so that others can grab it and hack on it.
If you choose to try it out, be aware of this.


Questions, Comments, etc?
-----------------------------------------------------------------------------------------------------
My hope is that Twython is so simple that you'd never *have* to ask any questions, but if
you feel the need to contact me for this (or other) reasons, you can hit me up
at ryan@venodesigns.net.

Twython is released under an MIT License - see the LICENSE file for more information.
