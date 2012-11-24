from django.conf.urls.defaults import *
from merkabah.admin import views as admin_views

from plugins.blog import urls as plugin_urls

urlpatterns = patterns('merkabah.admin.views',
    url(r'^$', admin_views.IndexCtrl.as_view(), name=admin_views.IndexCtrl.view_name),    
)

urlpatterns += plugin_urls.urlpatterns
