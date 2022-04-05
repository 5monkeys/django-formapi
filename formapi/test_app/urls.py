from django.urls import include, re_path

urlpatterns = [re_path(r"^api/", include("formapi.urls"))]
