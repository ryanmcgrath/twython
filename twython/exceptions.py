from .endpoints import twitter_http_status_codes


class TwythonError(Exception):
    """
        Generic error class, catch-all for most Twython issues.
        Special cases are handled by TwythonAuthError & TwythonRateLimitError.

        Note: Syntax has changed as of Twython 1.3. To catch these,
              you need to explicitly import them into your code, e.g:

        from twython import (
            TwythonError, TwythonRateLimitError, TwythonAuthError
        )
    """
    def __init__(self, msg, error_code=None, retry_after=None):
        self.error_code = error_code

        if error_code is not None and error_code in twitter_http_status_codes:
            msg = 'Twitter API returned a %s (%s), %s' % \
                  (error_code,
                   twitter_http_status_codes[error_code][0],
                   msg)

        super(TwythonError, self).__init__(msg)

    @property
    def msg(self):
        return self.args[0]


class TwythonAuthError(TwythonError):
    """ Raised when you try to access a protected resource and it fails due to
        some issue with your authentication.
    """
    pass


class TwythonRateLimitError(TwythonError):
    """ Raised when you've hit a rate limit.

        The amount of seconds to retry your request in will be appended
        to the message.
    """
    def __init__(self, msg, error_code, retry_after=None):
        if isinstance(retry_after, int):
            msg = '%s (Retry after %d seconds)' % (msg, retry_after)
        TwythonError.__init__(self, msg, error_code=error_code)
