.. special-functions:

Special Functions
=================

This section covers methods to are part of Twython but not necessarily connected to the Twitter API.

*******************************************************************************

Cursor
------

This function returns a generator for Twitter API endpoints that are able to be pagintated in some way (either by cursor or since_id parameter)

The Old Way
^^^^^^^^^^^

.. code-block:: python

    from twython import Twython

    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    results = twitter.search(q='twitter')
    if results.get('statuses'):
        for result in results['statuses']:
            print result['id_str']

The New Way
^^^^^^^^^^^

.. code-block:: python

    from twython import Twython

    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    results = twitter.cursor(twitter.search, q='twitter')
    for result in results:
        print result['id_str']

Another example:

.. code-block:: python

    results = twitter.cursor(t.get_mentions_timeline)
    for result in results:
        print result['id_str']


HTML for Tweet
--------------

This function takes a tweet object received from the Twitter API and returns an string formatted in HTML with the links, user mentions and hashtags replaced.

.. code-block:: python

    from twython import Twython

    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    user_tweets = twitter.get_user_timeline(screen_name='mikehelmick',
                                            include_rts=True)
    for tweet in user_tweets:
        tweet['text'] = Twython.html_for_tweet(tweet)
        print tweet['text']

The above code takes all the tweets from a specific users timeline, loops over them and replaces the value of ``tweet['text']`` with HTML.

So:

    http://t.co/FCmXyI6VHd is a #cool site, lol! @mikehelmick shd #checkitout. Love, @__twython__ https://t.co/67pwRvY6z9 http://t.co/N6InAO4B71

will be replaced with:

    <a href="http://t.co/FCmXyI6VHd" class="twython-url">google.com</a> is a <a href="https://twitter.com/search?q=%23cool" class="twython-hashtag">#cool</a> site, lol! <a href="https://twitter.com/mikehelmick" class="twython-mention">@mikehelmick</a> shd <a href="https://twitter.com/search?q=%23checkitout" class="twython-hashtag">#checkitout</a>. Love, <a href="https://twitter.com/__twython__" class="twython-mention">@__twython__</a> <a href="https://t.co/67pwRvY6z9" class="twython-url">github.com</a> <a href="http://t.co/N6InAO4B71" class="twython-media">pic.twitter.com/N6InAO4B71</a>

.. note:: When converting the string to HTML we add a class to each HTML tag so that you can maninpulate the DOM later on.

- For urls that are replaced we add ``class="twython-url"`` to the anchor tag
- For media urls that are replaced we add ``class="twython-media"`` to the anchor tag
- For user mentions that are replaced we add ``class="twython-mention"`` to the anchor tag
- For hashtags that are replaced we add ``class="twython-hashtag"`` to the anchor tag

This function accepts two parameters: ``use_display_url`` and ``use_expanded_url``
By default, ``use_display_url`` is ``True``. Meaning the link displayed in the tweet text will appear as (ex. google.com, github.com)
If ``use_expanded_url`` is ``True``, it overrides ``use_display_url``. The urls will then be displayed as (ex. http://google.com, https://github.com)
If ``use_display_url`` and ``use_expanded_url`` are ``False``, short url will be used (t.co/xxxxx)
