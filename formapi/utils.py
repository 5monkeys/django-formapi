import hashlib
import hmac
import uuid
from urllib.parse import quote

from django.utils.encoding import force_str, smart_bytes, smart_str


def get_sign(secret, querystring=None, **params):
    """
    Return sign for querystring.

    Logic:
    - Sort querystring by parameter keys and by value if two or more parameter keys share the same name
    - URL encode sorted querystring
    - Generate a hex digested hmac/sha1 hash using given secret
    """
    if querystring:
        params = dict(param.split("=") for param in querystring.split("&"))
    sorted_params = []
    for key, value in sorted(params.items(), key=lambda x: x[0]):
        if isinstance(value, (bytes, str)):
            sorted_params.append((key, value))
        else:
            try:
                value = list(value)
            except TypeError as e:
                assert "is not iterable" in smart_str(e)
                value = smart_bytes(value)
                sorted_params.append((key, value))
            else:
                sorted_params.extend((key, item) for item in sorted(value))
    return get_pairs_sign(secret, sorted_params)


def get_pairs_sign(secret, sorted_pairs):
    param_list = ("=".join((field, force_str(value))) for field, value in sorted_pairs)
    validation_string = smart_bytes("&".join(param_list))
    validation_string = smart_bytes(quote(validation_string))
    return hmac.new(smart_bytes(secret), validation_string, hashlib.sha1).hexdigest()


def prepare_uuid_string(value, default=None):
    if isinstance(value, uuid.UUID):
        value = value.hex
    if not value:
        return default
    value = str(value).replace("-", "").strip().lower()
    return value
