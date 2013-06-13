.. _streaming-api:

Streaming API
=============

This section will cover how to use Twython and interact with the Twitter Streaming API.

Streaming Documentation: https://dev.twitter.com/docs/streaming-apis

.. important:: The Streaming API requires that you have OAuth 1 authentication credentials. If you don't have credentials, head over to the :ref:`authentication section <oauth1>` and find out how!

Setting Up Your Streamer
------------------------

.. note:: When stream data is sent back to Twython, we send the data through signals (i.e. ``on_success``, ``on_error``, etc.)

Make sure you import ``TwythonStreamer``

.. code-block:: python

    from twython import TwythonStreamer

Now set up how you want to handle the signals.

.. code-block:: python

    class MyStreamer(TwythonStreamer):
        def on_success(self, data):
            if 'text' in data:
                print data['text'].encode('utf-8')

        def on_error(self, status_code, data):
            print status_code

            # Want to stop trying to get data because of the error?
            # Uncomment the next line!
            # self.disconnect()

More signals that you can extend on can be found in the Developer Interface section under :ref:`Streaming Interface <streaming_interface>`

Filtering Public Statuses
-------------------------

.. code-block:: python

    stream = MyStreamer(APP_KEY, APP_SECRET,
                        OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track='twitter')

With the code above, data should be flowing in.

