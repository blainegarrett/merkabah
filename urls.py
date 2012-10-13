'''
Pre-described urls
'''
from __future__ import absolute_import
import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^%s' % settings.MERKABAH_ADMIN_URL, include('merkabah.admin.urls')),
)