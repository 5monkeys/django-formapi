# coding=utf-8
# flake8: noqa
import sys
import django

if sys.version_info >= (3,):
    from django.utils.encoding import smart_bytes as smart_b, force_str as force_u, smart_text as smart_u
    # noinspection PyUnresolvedReferences
    from urllib.parse import quote
    ifilter = filter
    b_str = bytes
    u_str = str
    iteritems = lambda dic: dic.items()
else:
    from django.utils.encoding import smart_str as smart_b, force_unicode as force_u
    if django.VERSION >= (1, 4):
        from django.utils.encoding import smart_text as smart_u
    else:
        from django.utils.encoding import smart_unicode as smart_u
    # noinspection PyUnresolvedReferences
    from urllib2 import quote
    # noinspection PyUnresolvedReferences
    from itertools import ifilter
    b_str = str
    # noinspection PyUnresolvedReferences
    u_str = unicode
    iteritems = lambda dic: dic.iteritems()


if django.VERSION < (1, 5):
    # noinspection PyDeprecation
    from django.conf.urls.defaults import patterns, url, include
elif django.VERSION < (1, 10):
    from django.conf.urls import patterns, url, include
else:
    from django.conf.urls import url, include

    def patterns(prefix, *urls):
        assert not prefix
        return list(urls)


if django.VERSION < (1, 7):
    def get_user_model():
        from django.contrib.auth.models import User
        return User
else:
    from django.contrib.auth import get_user_model


if django.VERSION < (1, 9):
    from django.utils.importlib import import_module
else:
    from importlib import import_module


# Calm down unused import warnings:
assert len([
    smart_b, smart_u, force_u, quote, ifilter, get_user_model, import_module,
    patterns, url, include
])
