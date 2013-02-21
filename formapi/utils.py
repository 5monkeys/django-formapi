import hmac
import urllib2
from hashlib import sha1


def get_sign(secret, querystring=None, **params):
    """
    Return sign for querystring.

    Logic:
    - Sort querystring by parameter keys
    - URL encode sorted querystring
    - Generate a hex digested hmac/sha1 hash using given secret
    """
    if querystring:
        params = dict(param.split('=') for param in querystring.split('&'))
    sorted_params = ((key, str(params[key])) for key in sorted(params.keys()))
    validation_string = '&'.join(('='.join((field, value)) for field, value in sorted_params))
    return hmac.new(str(secret), urllib2.quote(validation_string), sha1).hexdigest()
