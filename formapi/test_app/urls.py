from ..compat import include, patterns, url

urlpatterns = patterns("", url(r"^api/", include("formapi.urls")))
