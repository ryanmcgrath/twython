.. :changelog:

History
-------

2.10.1 (2013-05-xx)
++++++++++++++++++
- More test coverage!
- Fix ``search_gen``
- Fixed ``get_lastfunction_header`` to actually do what its docstring says, returns ``None`` if header is not found
- Updated some internal API code, ``__init__`` didn't need to have ``self.auth`` and ``self.headers`` because they were never used anywhere else but the ``__init__``
- Added ``disconnect`` method to ``TwythonStreamer``, allowing users to disconnect as they desire
- Updated ``TwythonStreamError`` docstring, also allow importing it from ``twython``

2.10.0 (2013-05-21)
++++++++++++++++++
- Added ``get_retweeters_ids`` method
- Fixed ``TwythonDeprecationWarning`` on camelCase functions if the camelCase was the same as the PEP8 function (i.e. ``Twython.retweet`` did not change)
- Fixed error message bubbling when error message returned from Twitter was not an array (i.e. if you try to retweet something twice, the error is not found at index 0)
- Added "transparent" parameters for making requests, meaning users can pass bool values (True, False) to Twython methods and we convert your params in the background to satisfy the Twitter API. Also, file objects can now be passed seamlessly (see examples in README and in /examples dir for details)
- Callback URL is optional in ``get_authentication_tokens`` to accomedate those using OOB authorization (non web clients)
- Not part of the python package, but tests are now available along with Travis CI hooks
- Added ``__repr__`` definition for Twython, when calling only returning <Twython: APP_KEY>
- Cleaned up ``Twython.construct_api_url``, uses "transparent" parameters (see 4th bullet in this version for explaination)
- Update ``requests`` and ``requests-oauthlib`` requirements, fixing posting files AND post data together, making authenticated requests in general in Python 3.3

2.9.1 (2013-05-04)
++++++++++++++++++

- "PEP8" all the functions. Switch functions from camelCase() to underscore_funcs(). (i.e. ``updateStatus()`` is now ``update_status()``)

2.9.0 (2013-05-04)
++++++++++++++++++

- Fixed streaming issue #144, added ``TwythonStreamer`` to aid users in a friendly streaming experience (streaming examples in ``examples`` and README's have been updated as well)
- ``Twython`` now requires ``requests-oauthlib`` 0.3.1, fixes #154 (unable to upload media when sending POST data with the file)

2.8.0 (2013-04-29)
++++++++++++++++++

- Added a ``HISTORY.rst`` to start tracking history of changes
- Updated ``twitter_endpoints.py`` to ``endpoints.py`` for cleanliness
- Removed twython3k directory, no longer needed
- Added ``compat.py`` for compatability with Python 2.6 and greater
- Added some ascii art, moved description of Twython and ``__author__`` to ``__init__.py``
- Added ``version.py`` to store the current Twython version, instead of repeating it twice -- it also had to go into it's own file because of dependencies of ``requests`` and ``requests-oauthlib``, install would fail because those libraries weren't installed yet (on fresh install of Twython)
- Removed ``find_packages()`` from ``setup.py``, only one package (we can just define it)
- added quick publish method for Ryan and I: ``python setup.py publish`` is faster to type and easier to remember than ``python setup.py sdist upload``
- Removed ``base_url`` from ``endpoints.py`` because we're just repeating it in ``Twython.__init__``
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
