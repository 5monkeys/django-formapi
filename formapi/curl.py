#!/usr/bin/env python

"""curl wrapper for signing with formapi key & secret"""

import os
import sys
import hmac
import urllib
import base64
import hashlib
import logging
import urlparse

log = logging.getLogger('curl-formapi')
configure_logging = lambda level: logging.basicConfig(level=level)

try:
    import interpress.logutils as LU
except ImportError:
    pass
else:
    configure_logging = lambda level: LU.basic_config(level=level)

def find_opts(args=sys.argv[1:]):
    """args -> {opt: [value, ...], ...}, [nonopt_arg, ...]"""

    state = 0
    opts = {}
    nonopts = []

    for arg in args:

        if state == 0:
            parts = arg.split('=', 1)
            head, tail = parts[0], parts[1:]

            if head not in ('--key', '--secret', '--debug', '-F'):
                nonopts.append(arg)
                continue

            key = head.lstrip('-')
            if tail:
                opts.setdefault(key, ''.join(tail))
            else:
                state = 'next:' + key

        else:
            key = state[5:]
            opts.setdefault(key, []).append(arg)
            state = 0

    return opts, nonopts


def print_help(missing=None):
    print >>sys.stderr, 'usage: curl-formapi --secret=SECRET --key=KEY [-F A=B ...] URL'
    if missing:
        print >>sys.stderr, 'missing ' + ', '.join(sorted(missing))


def main():
    opts, args = find_opts()

    missing = {'key', 'secret'} - set(opts)
    if missing:
        print_help(missing=missing)
        sys.exit(1)

    key, secret = opts['key'][-1], opts['secret'][-1]
    url = urlparse.urlsplit(args[-1])
    query_items = url.query.split('&')
    form_items = opts['F']

    configure_logging(logging.DEBUG if opts.get('debug') else logging.INFO)
    log.debug('opts, args = %s, %s', opts, args)

    sign_items = filter(None, sorted(query_items + form_items))
    msg = urllib.quote('&'.join(sign_items))
    log.debug('msg = %r', msg)

    h = hmac.new(secret, msg=msg, digestmod=hashlib.sha1)
    sig = base64.urlsafe_b64encode(h.digest())[:int(h.digest_size*8/6)]
    log.debug('sig = %s', sig)

    query_signed = '&'.join(filter(None, query_items + ['key=' + key, 'sign=' + sig]))
    url_signed = urlparse.urlunsplit((url.scheme, url.netloc, url.path, query_signed, url.fragment))
    log.debug('url_signed = %s', url_signed)

    args[:0] = [arg for form_item in form_items for arg in ('-F', form_item)]
    args[-1:] = [url_signed]
    args[:0] = ['curl']

    log.debug('invoking curl: %s', args)
    os.execvp('curl', args)

if __name__ == "__main__":
    main()
