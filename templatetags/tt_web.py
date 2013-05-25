from django.template import Library, Node, Variable, TemplateSyntaxError, VariableDoesNotExist
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape

register = Library()

@register.simple_tag
def carousel():
    data = [{
                'title': u'Se\xf1or Wong Mural',
                'image_path' : '/static/mural2_.jpg',
                'description' : 'DUDE!!!!',
                'link' :  'http://google.com',
            }
            ,{
                'title': 'All Over the Walls',
                'image_path' : '/static/aotw_.jpg',
                'description' : 'sdddddddddd',
                'link' :  'http://google.com',
            },
            {
                'title': 'Live Painting',
                'image_path' : '/static/livingpainting_.jpg',
                'description' : 'sfsdfsdfdsfdsfsdfsdfdsfds',
                'link' :  'http://google.com',
            }]
            
    context = {'panels' : data}
    
    rendered_content = render_to_string("homepage_carousel.html", context)
    
    return rendered_content
    


@register.filter
def truncate(val, arg):
    if len(val) > arg - 3:
        return val[0:arg-1] + '...'
    return val