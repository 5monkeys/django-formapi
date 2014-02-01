# coding=utf-8
# flake8: noqa
import six

if six.PY3:
    from django.utils.encoding import smart_bytes as smart_str, force_str as force_unicode
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
    from django.conf.urls.defaults import patterns, url, include
