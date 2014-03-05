# coding=utf-8
import hmac
from hashlib import sha1
from .compat import force_unicode, smart_str, quote, basestring


def get_sign(secret, querystring=None, **params):
    """
    Return sign for querystring.

    Logic:
    - Sort querystring by parameter keys and by value if two or more parameter keys share the same name
    - URL encode sorted querystring
    - Generate a hex digested hmac/sha1 hash using given secret
    """
    if querystring:
        params = dict(param.split('=') for param in querystring.split('&'))
    sorted_params = []
    for key, value in sorted(params.items(), key=lambda x: x[0]):
        if isinstance(value, basestring):
            sorted_params.append((key, value))
        else:
            try:
                value = list(value)
            except TypeError as e:
                assert 'is not iterable' in str(e)
                value = smart_str(value)
                sorted_params.append((key, value))
            else:
                sorted_params.extend((key, item) for item in sorted(value))
    param_list = ('='.join((field, force_unicode(value))) for field, value in sorted_params)
    validation_string = smart_str('&'.join(param_list))
    validation_string = quote(validation_string)
    return hmac.new(smart_str(secret), validation_string, sha1).hexdigest()
