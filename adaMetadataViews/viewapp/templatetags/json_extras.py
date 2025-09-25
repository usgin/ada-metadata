import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def tojson(value):
    """Render a Python object as JSON without HTML escaping"""
    return mark_safe(json.dumps(value))