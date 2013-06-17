.. _api:

Developer Interface
===================

.. module:: twython

This page of the documentation will cover all methods and classes available to the developer.

Twython, currently, has two main interfaces:

- Twitter's Core API (updating statuses, getting timelines, direct messaging, etc)
- Twitter's Streaming API

Core Interface
--------------

.. autoclass:: Twython
   :special-members: __init__
   :inherited-members:

.. _streaming_interface:

Streaming Interface
-------------------

.. autoclass:: TwythonStreamer
   :special-members: __init__
   :inherited-members:

Streaming Types
~~~~~~~~~~~~~~~

.. autoclass:: twython.streaming.types.TwythonStreamerTypes
   :inherited-members:

.. autoclass:: twython.streaming.types.TwythonStreamerTypesStatuses
   :inherited-members:

Exceptions
----------

.. autoexception:: twython.TwythonError
.. autoexception:: twython.TwythonAuthError
.. autoexception:: twython.TwythonRateLimitError