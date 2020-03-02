# -*- coding: utf-8 -*-

"""
twython.advisory
~~~~~~~~~~~~~~~~

This module contains Warning classes for Twython to specifically
alert the user about.

This mainly is because Python 2.7 > mutes DeprecationWarning and when
we deprecate a method or variable in Twython, we want to use to see
the Warning but don't want ALL DeprecationWarnings to appear,
only TwythonDeprecationWarnings.
"""


class TwythonDeprecationWarning(DeprecationWarning):
    """Custom DeprecationWarning to be raised when methods/variables
    are being deprecated in Twython. Python 2.7 > ignores DeprecationWarning
    so we want to specifically bubble up ONLY Twython Deprecation Warnings
    """
    pass
