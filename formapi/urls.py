try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url
from .api import API


urlpatterns = patterns('',
    url(r'discover/$', 'formapi.views.discover', name='api_discover'),
    url(r'call/(?P<version>.+)/(?P<namespace>\w+)/(?P<call_name>\w+)/$', 'formapi.views.call', name='api_call'),
    url(r'(?P<version>.+)/(?P<namespace>\w+)/(?P<call>\w+)/', API.as_view(), name='api_view'),
)
