# coding=utf8
import django
from django import template

register = template.Library()

if django.VERSION < (1, 5):
    from django.templatetags import future

    @register.tag
    def url(parser, token):
        return future.url(parser=parser, token=token)


@register.filter
def as_dict(obj):
    return dict(obj)
