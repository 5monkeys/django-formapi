# coding=utf-8
from .api import API
from .compat import patterns, url


urlpatterns = patterns('',
    url(r'discover/$', 'formapi.views.discover', name='api_discover'),
    url(r'call/(?P<version>.+)/(?P<namespace>\w+)/(?P<call_name>\w+)/$', 'formapi.views.call', name='api_call'),
    url(r'(?P<version>.+)/(?P<namespace>\w+)/(?P<call>\w+)/', API.as_view(), name='api_view'),
)
