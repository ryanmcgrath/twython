.. :changelog:

History
-------

3.1.2 (2013-12-05)
++++++++++++++++++

- Fixed Changelog (HISTORY.rst)

3.1.1 (2013-12-05)
++++++++++++++++++

- Update `requests` version to 2.1.0.
- Fixed: Streaming issue where `Exceptions` in handlers or `on_success` which subclass `ValueError` would previously be caught and reported as a JSON decoding problem, and `on_error()` would be called (with status_code=200)
- Fixed issue where XML was returned when bad tokens were passed to `get_authorized_tokens`
- Fixed import for `setup` causing installation to fail on some devices (eg. Nokia N9/MeeGo)

3.1.0 (2013-09-25)
++++++++++++++++++

- Added ``html_for_tweet`` static method. This method accepts a tweet object returned from a Twitter API call and will return a string with urls, mentions and hashtags in the tweet replaced with HTML.
- Pass ``client_args`` to the streaming ``__init__``, much like in core Twython (you can pass headers, timeout, hooks, proxies, etc.).
- Streamer has new parameter ``handlers`` which accepts a list of strings related to functions that are apart of the Streaming class and start with "on\_". i.e. ['delete'] is passed, when 'delete' is received from a stream response; ``on_delete`` will be called.
- When an actual request error happens and a ``RequestException`` is raised, it is caught and a ``TwythonError`` is raised instead for convenience.
- Added "cursor"-like functionality. Endpoints with the attribute ``iter_mode`` will be able to be passed to ``Twython.cursor`` and returned as a generator.
- ``Twython.search_gen`` has been deprecated. Please use ``twitter.cursor(twitter.search, q='your_query')`` instead, where ``twitter`` is your ``Twython`` instance.
- Added methods ``get_list_memberships``, ``get_twitter_configuration``, ``get_supported_languages``, ``get_privacy_policy``, ``get_tos``
- Added ``auth_endpoint`` parameter to ``Twython.__init__`` for cases when the right parameters weren't being shown during the authentication step.
- Fixed streaming issue where results wouldn't be returned for streams that weren't so active (See https://github.com/ryanmcgrath/twython/issues/202#issuecomment-19915708)
- Streaming API now uses ``_transparent_params`` so when passed ``True`` or ``False`` or an array, etc. Twython formats it to meet Twitter parameter standards (i.e. ['ryanmcgrath', 'mikehelmick', 'twitterapi'] would convert to string 'ryanmcgrath,mikehelmick,twitterapi')

3.0.0 (2013-06-18)
++++++++++++++++++

- Changed ``twython/twython.py`` to ``twython/api.py`` in attempt to make structure look a little neater
- Removed all camelCase function access (anything like ``getHomeTimeline`` is now ``get_home_timeline``)
- Removed ``shorten_url``. With the ``requests`` library, shortening a URL on your own is simple enough
- ``twitter_token``, ``twitter_secret`` and ``callback_url`` are no longer passed to ``Twython.__init__``
    - ``twitter_token`` and ``twitter_secret`` have been replaced with ``app_key`` and ``app_secret`` respectively
    - ``callback_url`` is now passed through ``Twython.get_authentication_tokens``
- Update ``test_twython.py`` docstrings per http://www.python.org/dev/peps/pep-0257/
- Removed ``get_list_memberships``, method is Twitter API 1.0 deprecated
- Developers can now pass an array as a parameter to Twitter API methods and they will be automatically joined by a comma and converted to a string
- ``endpoints.py`` now contains ``EndpointsMixin`` (rather than the previous ``api_table`` dict) for Twython, which enables Twython to use functions declared in the Mixin.
- Added OAuth 2 authentication (Application Only) for when you want to make read-only calls to Twitter without having to go through the whole user authentication ritual (see docs for usage)
- Added ``obtain_access_token`` to obtain an OAuth 2 Application Only read-only access token
- ``construct_api_url`` now accepts keyword arguments like other Twython methods (e.g. instead of passing ``{'q': 'twitter', 'result_type': 'recent'}``, pass ``q='twitter', result_type='recent'``)
- Pass ``client_args`` to the Twython ``__init__`` to manipulate request variables. ``client_args`` accepts a dictionary of keywords and values that accepted by ``requests`` (`Session API <http://docs.python-requests.org/en/latest/api/#sessionapi>`_) [ex. headers, proxies, verify(SSL verification)] and the "request" section directly below it.
- Added ``get_application_rate_limit_status`` API method for returning the current rate limits for the specified source
- Added ``invalidate_token`` API method which allows registed apps to revoke an access token presenting its client credentials
- ``get_lastfunction_header`` now accepts a ``default_return_value`` parameter. This means that if you pass a second value (ex. ``Twython.get_lastfunction_header('x-rate-limit-remaining', 0)``) and the value is not found, it returns your default value

2.10.1 (2013-05-29)
++++++++++++++++++

- More test coverage!
- Fix ``search_gen``
- Fixed ``get_lastfunction_header`` to actually do what its docstring says, returns ``None`` if header is not found
- Updated some internal API code, ``__init__`` didn't need to have ``self.auth`` and ``self.headers`` because they were never used anywhere else but the ``__init__``
- Added ``disconnect`` method to ``TwythonStreamer``, allowing users to disconnect as they desire
- Updated ``TwythonStreamError`` docstring, also allow importing it from ``twython``
- No longer raise ``TwythonStreamError`` when stream line can't be decoded. Instead, sends signal to ``TwythonStreamer.on_error``
- Allow for (int, long, float) params to be passed to Twython Twitter API functions in Python 2, and (int, float) in Python 3

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
