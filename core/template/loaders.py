"""
Merkabah Template Loaders
"""
from django.template import TemplateDoesNotExist
import settings


def load_template_source(template_name, template_dirs=None):
    """
    Loader for Merkabah templates
    """

    if (template_name.find('merkabah/') == 0):
        template_name = '%stemplates/%s' % (settings.MERKABAH_PATH, template_name[9:])

        try:
            return open(template_name).read(), template_name
        except IOError:
            pass

    if (template_name.find('plugins/') == 0):
        # This is loading the default plugin templates

        chunks = template_name.split('/')
        plugin_module = chunks[1]

        # Check if this is an installed plugin
        if plugin_module in settings.INSTALLED_PLUGINS:
            pt_path = '%s/%s/templates' % (settings.PLUGIN_PATH, plugin_module)
            t_path = '/'.join(chunks[2:])
            template_name = '%s/%s' % (pt_path, t_path)

            try:
                return open(template_name).read(), template_name
            except IOError:
                pass

    raise TemplateDoesNotExist(template_name)

load_template_source.is_usable = True
