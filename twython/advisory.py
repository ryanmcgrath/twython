class TwythonDeprecationWarning(DeprecationWarning):
    """Custom DeprecationWarning to be raised when methods/variables are being deprecated in Twython.
    Python 2.7 > ignores DeprecationWarning so we want to specifcally bubble up ONLY Twython Deprecation Warnings
    """
    pass
