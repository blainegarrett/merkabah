from django.template import TemplateDoesNotExist
import logging
import settings

def load_template_source(template_name, template_dirs=None):
    '''
    Loader for Merkabah templates
    '''
    
    if (template_name.find('merkabah/') == 0):
        template_name = '%stemplates/%s' % (settings.MERKAHBAH_PATH, template_name[9:])
        
        logging.warning(template_name)
        
        try:
            return open(template_name).read(), template_name
        except IOError:
            logging.error(template_name)
            pass
    raise TemplateDoesNotExist, template_name
    
load_template_source.is_usable = True