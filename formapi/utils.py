import hmac
import urllib2
from hashlib import sha1
from django.utils.encoding import force_unicode

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
    sorted_params = ((key, params[key]) for key in sorted(params.keys()))
    param_list = ('='.join((field, force_unicode(value))) for field, value in sorted_params)
    validation_string = force_unicode('&'.join(param_list))
    return hmac.new(str(secret), urllib2.quote(validation_string.encode('utf-8')), sha1).hexdigest()
