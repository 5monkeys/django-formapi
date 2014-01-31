try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('', url(r'^api/', include('formapi.urls')))
