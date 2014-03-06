# coding=utf-8
# flake8: noqa
import sys

if sys.version_info[0] == 3:
    from django.utils.encoding import smart_bytes as smart_b, force_str as force_u, smart_text as smart_u
    # noinspection PyUnresolvedReferences
    from urllib.parse import quote
    ifilter = filter
    b_str = bytes
    u_str = str
    iteritems = lambda dic: dic.items()
else:
    from django.utils.encoding import smart_str as smart_b, force_unicode as force_u
    try:
        from django.utils.encoding import smart_text as smart_u
    except:
        # Django 1.3
        from django.utils.encoding import smart_unicode as smart_u
    # noinspection PyUnresolvedReferences
    from urllib2 import quote
    # noinspection PyUnresolvedReferences
    from itertools import ifilter
    b_str = str
    # noinspection PyUnresolvedReferences
    u_str = unicode
    iteritems = lambda dic: dic.iteritems()

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    # noinspection PyUnresolvedReferences
    from django.conf.urls.defaults import patterns, url, include


# Calm down unused import warnings:
assert [smart_b, smart_u, force_u, quote, ifilter]
