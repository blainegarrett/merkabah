"""
Merkabah Base Settings
"""
import os.path
ROOT_URLCONF = 'urls'
DEBUG=True
APPEND_SLASH = True
PROJECT_DIR = os.path.dirname(__file__) # this is not Django setting.
TEMPLATE_DIRS = (os.path.join(PROJECT_DIR, "merkabah/templates"),)

INSTALLED_APPS = ('merkabah')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'merkabah.core.template.loaders.load_template_source',
)

MERKABAH_ADMIN_URL = 'admin'
