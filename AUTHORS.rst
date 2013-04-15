Special Thanks
--------------
This is a list of all those who have contributed code to Twython in some way, shape, or form. I think it's
exhaustive, but I could be wrong - if you think your name should be here and it's not, please contact
me and let me know (or just issue a pull request on GitHub, and leave a note about it so I can just accept it ;).

Development Lead
````````````````

- Ryan Mcgrath <ryan@venodesigns.net>


Patches and Suggestions
````````````````````````

- `Mike Helmick <https://github.com/michaelhelmick>`_, multiple fixes and proper ``requests`` integration. Too much to list here.
- `kracekumar <https://github.com/kracekumar>`_, early ``requests`` work and various fixes.
- `Erik Scheffers <https://github.com/eriks5>`_, various fixes regarding OAuth callback URLs.
- `Jordan Bouvier <https://github.com/jbouvier>`_, various fixes regarding OAuth callback URLs.
- `Dick Brouwer <https://github.com/dikbrouwer>`_, fixes for OAuth Verifier in ``get_authorized_tokens``.
- `hades <https://github.com/hades>`_, Fixes to various initial OAuth issues and keeping ``Twython3k`` up-to-date.
- `Alex Sutton <https://github.com/alexsdutton/twython/>`_, fix for parameter substitution regular expression (catch underscores!).
- `Levgen Pyvovarov <https://github.com/bsn>`_, Various argument fixes, cyrillic text support.
- `Mark Liu <https://github.com/mliu7>`_, Missing parameter fix for ``addListMember``.
- `Randall Degges <https://github.com/rdegge>`_, PEP-8 fixes, MANIFEST.in, installer fixes.
- `Idris Mokhtarzada <https://github.com/idris>`_, Fixes for various example code pieces.
- `Jonathan Elsas <https://github.com/jelsas>`_, Fix for original Streaming API stub causing import errors.
- `LuqueDaniel <https://github.com/LuqueDaniel>`_, Extended example code where necessary.
- `Mesar Hameed <https://github.com/mhameed>`_, Commit to swap ``__getattr__`` trick for a more debuggable solution.
- `Remy DeCausemaker <https://github.com/decause>`_, PEP-8 contributions.
- `mckellister <https://github.com/mckellister>`_ Twitter Spring 2012 Clean Up fixes to ``Exception`` raised by Twython (Rate Limits, etc).
- `Tatz Tsuchiya <http://d.hatena.ne.jp/tatz_tsuchiya/20120115/1326623451>`_, Fix for ``lambda`` scoping in key injection phase.
- `Mohammed ALDOUB <https://github.com/Voulnet>`_, Fixes for ``http/https`` access endpoints.
- `Fumiaki Kinoshita <https://github.com/fumieval>`_, Re-added Proxy support for 2.3.0.
- `Terry Jones <https://github.com/terrycojones>`_, Error cleanup and Exception processing in 2.3.0.
- `Leandro Ferreira <https://github.com/leandroferreira>`_, Fix for double-encoding of search queries in 2.3.0.
- `Chris Brown <https://github.com/chbrown>`_, Updated to use v1.1 endpoints over v1
- `Virendra Rajput <https://github.com/bkvirendra>`_, Fixed unicode (json) encoding in twython.py 2.7.2.  
- `Paul Solbach <https://github.com/hansenrum>`_, fixed requirement for oauth_verifier
- `Greg Nofi <https://github.com/nofeet>`_, fixed using built-in Exception attributes for storing & retrieving error message
