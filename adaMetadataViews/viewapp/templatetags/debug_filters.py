from django import template
import pprint

register = template.Library()

@register.filter
def debug(value):
    """Pretty-print Python objects for debugging in templates."""
    print('debug print:' + pprint.pformat(value))
    return pprint.pformat(value)