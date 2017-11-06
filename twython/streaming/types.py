# -*- coding: utf-8 -*-

"""
twython.streaming.types
~~~~~~~~~~~~~~~~~~~~~~~

This module contains classes and methods for :class:`TwythonStreamer` to use.
"""


class TwythonStreamerTypes(object):
    """Class for different stream endpoints

    Not all streaming endpoints have nested endpoints.
    User Streams and Site Streams are single streams with no nested endpoints
    Status Streams include filter, sample and firehose endpoints

    """
    def __init__(self, streamer):
        self.streamer = streamer
        self.statuses = TwythonStreamerTypesStatuses(streamer)

    def user(self, **params):
        """Stream user

        Accepted params found at:
        https://dev.twitter.com/docs/api/1.1/get/user
        """
        url = 'https://userstream.twitter.com/%s/user.json' \
              % self.streamer.api_version
        self.streamer._request(url, params=params)

    def site(self, **params):
        """Stream site

        Accepted params found at:
        https://dev.twitter.com/docs/api/1.1/get/site
        """
        url = 'https://sitestream.twitter.com/%s/site.json' \
              % self.streamer.api_version
        self.streamer._request(url, params=params)


class TwythonStreamerTypesStatuses(object):
    """Class for different statuses endpoints

    Available so :meth:`TwythonStreamer.statuses.filter()` is available.
    Just a bit cleaner than :meth:`TwythonStreamer.statuses_filter()`,
    :meth:`statuses_sample()`, etc. all being single methods in 
    :class:`TwythonStreamer`.

    """
    def __init__(self, streamer):
        self.streamer = streamer
        self.params = None

    def filter(self, **params):
        """Stream statuses/filter

        :param \*\*params: Parameters to send with your stream request

        Accepted params found at:
        https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter
        """
        url = 'https://stream.twitter.com/%s/statuses/filter.json' \
              % self.streamer.api_version
        self.streamer._request(url, 'POST', params=params)

    def sample(self, **params):
        """Stream statuses/sample

        :param \*\*params: Parameters to send with your stream request

        Accepted params found at:
        https://developer.twitter.com/en/docs/tweets/sample-realtime/api-reference/get-statuses-sample
        """
        url = 'https://stream.twitter.com/%s/statuses/sample.json' \
              % self.streamer.api_version
        self.streamer._request(url, params=params)

    def firehose(self, **params):
        """Stream statuses/firehose

        :param \*\*params: Parameters to send with your stream request

        Accepted params found at:
        https://dev.twitter.com/docs/api/1.1/get/statuses/firehose
        """
        url = 'https://stream.twitter.com/%s/statuses/firehose.json' \
              % self.streamer.api_version
        self.streamer._request(url, params=params)

    def set_dynamic_filter(self, **params):
        """Set/update statuses/filter

        :param \*\*params: Parameters to send with your stream request

        Accepted params found at:
        https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter
        """
        self.params = params

    def dynamic_filter(self):
        """Stream statuses/filter with dynamic parameters"""

        url = 'https://stream.twitter.com/%s/statuses/filter.json' \
              % self.streamer.api_version
        self.streamer._request(url, 'POST', params=self.params)
