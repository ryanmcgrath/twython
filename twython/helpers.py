from .compat import basestring, numeric_types


def _transparent_params(_params):
    params = {}
    files = {}
    for k, v in _params.items():
        if hasattr(v, 'read') and callable(v.read):
            files[k] = v
        elif isinstance(v, bool):
            if v:
                params[k] = 'true'
            else:
                params[k] = 'false'
        elif isinstance(v, basestring) or isinstance(v, numeric_types):
            params[k] = v
        else:
            continue
    return params, files
