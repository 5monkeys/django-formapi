from . import views
from .api import API
from .compat import patterns, url

urlpatterns = patterns(
    "",
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
)
