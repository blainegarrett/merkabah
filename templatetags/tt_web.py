from django.template import Library, Node, Variable, TemplateSyntaxError, VariableDoesNotExist
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape

register = Library()

@register.filter
def truncate(val, arg):
    if len(val) > arg - 3:
        return val[0:arg-1] + '...'
    return val