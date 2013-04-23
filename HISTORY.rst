History
-------

2.8.0 (2013-04-29)
++++++++++++++++++

- Added a ``HISTORY.rst`` to start tracking history of changes
- Updated ``twitter_endpoints.py`` to ``endpoints.py`` for cleanliness
- Removed twython3k directory, no longer needed
- Added ``compat.py`` for compatability with Python 2.6 and greater
- Added some ascii art, moved description of Twython and ``__author__`` to ``__init__.py``
- Added ``version.py`` to store the current Twython version, instead of repeating it twice -- it also had to go into it's own file because of dependencies of ``requests`` and ``requests-oauthlib``, install would fail because those libraries weren't installed yet (on fresh install of Twython)
- Removed ``find_packages()`` from ``setup.py``, only one package -- we can
just define it
- added quick publish method for Ryan and I: ``python setup.py publish`` is faster to type and easier to remember than ``python setup.py sdist upload``
- Removed ``base_url`` from ``endpoints.py`` because we're just repeating it in
``Twython.__init__``
- ``Twython.get_authentication_tokens()`` now takes ``callback_url`` argument rather than passing the ``callback_url`` through ``Twython.__init__``, ``callback_url`` is only used in the ``get_authentication_tokens`` method and nowhere else (kept in init though for backwards compatability)
- Updated README to better reflect current Twython codebase
- Added ``warnings.simplefilter('default')`` line in ``twython.py`` for Python 2.7 and greater to display Deprecation Warnings in console
- Added Deprecation Warnings for usage of ``twitter_token``, ``twitter_secret`` and ``callback_url`` in ``Twython.__init__``
- Headers now always include the User-Agent as Twython vXX unless User-Agent is overwritten
- Removed senseless TwythonError thrown if method is not GET or POST, who cares -- if the user passes something other than GET or POST just let Twitter return the error that they messed up
- Removed conversion to unicode of (int, bool) params passed to a requests. ``requests`` isn't greedy about variables that can't be converted to unicode anymore
- Removed `bulkUserLookup` (please use `lookupUser` instead), removed `getProfileImageUrl` (will be completely removed from Twitter API on May 7th, 2013)
- Updated shortenUrl to actually work for those using it, but it is being deprecated since `requests` makes it easy for developers to implement their own url shortening in their app (see https://github.com/ryanmcgrath/twython/issues/184)
- Twython Deprecation Warnings will now be seen in shell when using Python 2.7 and greater
- Twython now takes ``ssl_verify`` parameter, defaults True. Set False if you're having development server issues
- Removed internal ``_media_update`` function, we could have always just used ``self.post``

2.7.3 (2013-04-12)
++++++++++++++++++

- Fixed issue where Twython Exceptions were not being logged correctly

2.7.2 (2013-04-08)
++++++++++++++++++

- Fixed ``AttributeError`` when trying to decode the JSON response via ``Response.json()``

2.7.1 (2013-04-08)
++++++++++++++++++

- Removed ``simplejson`` dependency
- Fixed ``destroyDirectMessage``, ``createBlock``, ``destroyBlock`` endpoints in ``twitter_endpoints.py``
- Added ``getProfileBannerSizes`` method to ``twitter_endpoints.py``
- Made oauth_verifier argument required in ``get_authorized_tokens``
- Update ``updateProfileBannerImage`` to use v1.1 endpoint

2.7.0 (2013-04-04)
++++++++++++++++++

- New ``showOwnedLists`` method

2.7.0 (2013-03-31)
++++++++++++++++++

- Added missing slash to ``getMentionsTimeline`` in ``twitter_endpoints.py``

2.6.0 (2013-03-29)
++++++++++++++++++

- Updated ``twitter_endpoints.py`` to better reflect order of API endpoints on the Twitter API v1.1 docs site