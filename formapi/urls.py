from django.conf.urls import url

from . import views
from .api import API

urlpatterns = [
    url(r"discover/$", views.discover, name="api_discover"),
    url(
        r"call/(?P<version>.+)/(?P<namespace>\w+)/(?P<call_name>\w+)/$",
        views.call,
        name="api_call",
    ),
    url(
        r"(?P<version>.+)/(?P<namespace>\w+)/(?P<call>\w+)/",
        API.as_view(),
        name="api_view",
    ),
]
