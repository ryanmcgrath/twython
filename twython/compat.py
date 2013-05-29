import sys

_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

try:
    import simplejson as json
except ImportError:
    import json

if is_py2:
    from urllib import urlencode, quote_plus
    try:
        from urlparse import parse_qsl
    except ImportError:
        from cgi import parse_qsl

    str = unicode
    basestring = basestring
    numeric_types = (int, long, float)


elif is_py3:
    from urllib.parse import urlencode, quote_plus, parse_qsl

    str = str
    basestring = (str, bytes)
    numeric_types = (int, float)
