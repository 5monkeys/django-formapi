from django import template

register = template.Library()


@register.filter
def as_dict(obj):
    return dict(obj)
