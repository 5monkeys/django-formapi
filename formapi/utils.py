import hmac
import urllib2
from hashlib import sha1
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_unicode, force_text, force_bytes
from django.utils.http import urlencode, urlquote


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
    sorted_params = []
    for key, value in sorted(params.items(), key=lambda x: x[0]):
        if isinstance(value, basestring):
            sorted_params.append((key, value))
        else:
            try:
                value = list(value)
            except TypeError, e:
                assert 'is not iterable' in str(e)
                value = force_bytes(value)
                sorted_params.append((key, value))
            else:
                sorted_params.extend((key, item) for item in sorted(value))
    param_list = ('='.join((field, force_unicode(value))) for field, value in sorted_params)
    validation_string = force_bytes('&'.join(param_list))
    validation_string = urllib2.quote(validation_string)
    return hmac.new(str(secret), validation_string, sha1).hexdigest()
