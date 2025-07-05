from django import template

register = template.Library()

@register.filter
def first_value(d):
    if isinstance(d, dict):
        return next(iter(d.values()), "")
    return ""
