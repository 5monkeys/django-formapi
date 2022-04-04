from django.shortcuts import render

from .api import API


def discover(request):
    return render(
        request, "formapi/api/discover.html", {"mapping": dict(API.call_mapping)}
    )


def call(request, version, namespace, call_name):
    form_class = API.call_mapping[version][namespace][call_name]
    context = {
        "mapping": dict(API.call_mapping),
        "form_class": form_class,
        "version": version,
        "namespace": namespace,
        "call": call_name,
        "docstring": form_class.__doc__,
    }
    return render(request, "formapi/api/call.html", context)
