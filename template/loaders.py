from django.template import TemplateDoesNotExist
import logging
def load_template_source(template_name, template_dirs=None):
    '''
    Loader for Merkabah templates
    '''
    
    if (template_name.find('merkabah/') == 0):
        template_name = template_name[:9] + 'templates/' + template_name[9:]
        try:
            return open(template_name).read(), template_name
        except IOError:
            pass
    raise TemplateDoesNotExist, template_name
    
load_template_source.is_usable = True