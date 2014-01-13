# -*- coding: utf-8 -*-

"""
twython.exceptions
~~~~~~~~~~~~~~~~~~

This module contains Twython specific Exception classes.
"""

from .endpoints import TWITTER_HTTP_STATUS_CODE


class TwythonError(Exception):
    """Generic error class, catch-all for most Twython issues.
    Special cases are handled by TwythonAuthError & TwythonRateLimitError.

    from twython import TwythonError, TwythonRateLimitError, TwythonAuthError

    """
    def __init__(self, msg, error_code=None, retry_after=None):
        self.error_code = error_code

        if error_code is not None and error_code in TWITTER_HTTP_STATUS_CODE:
            msg = 'Twitter API returned a %s (%s), %s' % \
                  (error_code,
                   TWITTER_HTTP_STATUS_CODE[error_code][0],
                   msg)

        super(TwythonError, self).__init__(msg)

    @property
    def msg(self):  # pragma: no cover
        return self.args[0]


class TwythonAuthError(TwythonError):
    """Raised when you try to access a protected resource and it fails due to
    some issue with your authentication.

    """
    pass


class TwythonRateLimitError(TwythonError):  # pragma: no cover
    """Raised when you've hit a rate limit.

    The amount of seconds to retry your request in will be appended
    to the message.

    """
    def __init__(self, msg, error_code, retry_after=None):
        if isinstance(retry_after, int):
            msg = '%s (Retry after %d seconds)' % (msg, retry_after)
        TwythonError.__init__(self, msg, error_code=error_code)

        self.retry_after = retry_after


class TwythonStreamError(TwythonError):
    """Raised when an invalid response from the Stream API is received"""
    pass
