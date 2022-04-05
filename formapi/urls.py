from django.urls import re_path

from . import views
from .api import API

urlpatterns = [
    re_path(r"discover/$", views.discover, name="api_discover"),
    re_path(
        r"call/(?P<version>.+)/(?P<namespace>\w+)/(?P<call_name>\w+)/$",
        views.call,
        name="api_call",
    ),
    re_path(
        r"(?P<version>.+)/(?P<namespace>\w+)/(?P<call>\w+)/",
        API.as_view(),
        name="api_view",
    ),
]
