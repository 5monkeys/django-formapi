# coding=utf-8
# flake8: noqa
import sys

if sys.version_info[0] == 3:
    from django.utils.encoding import smart_bytes as smart_str, force_str as force_unicode
    # noinspection PyUnresolvedReferences
    from urllib.parse import quote
    basestring = (str, bytes)
    ifilter = filter
    unicode = str
else:
    from django.utils.encoding import smart_str, force_unicode
    from urllib2 import quote
    from itertools import ifilter
    basestring = basestring
    unicode = unicode

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    # noinspection PyUnresolvedReferences
    from django.conf.urls.defaults import patterns, url, include


# Calm down unused import warnings:
assert [smart_str, force_unicode, quote, ifilter]
