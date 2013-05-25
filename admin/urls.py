from django.conf.urls.defaults import *
from merkabah.admin import controllers as ac

urlpatterns = patterns('merkabah.admin.views',
    url(r'^$', ac.IndexCtrl.as_django_view(), name=ac.IndexCtrl.view_name),
    
    url(r'^plugin/(?P<plugin_slug>[A-Za-z0-9-_]+)/$', ac.PluginIndexCtrl.as_django_view(), name=ac.PluginIndexCtrl.view_name),
    url(r'^plugin/(?P<plugin_slug>[A-Za-z0-9-_]+)/(?P<action>[A-Za-z0-9-_]+)/$', ac.PluginActionCtrl.as_django_view(), name=ac.PluginActionCtrl.view_name),

#    url(r'^plugin/(?P<plugin>[A-Za-z0-9-_/:]+)/$', admin_views.PluginCtrl.as_django_view(), name=admin_views.PluginCtrl.view_name),   
#    (r'^gallery/(?P<page_key>[A-Za-z0-9-_/:]+)/$', 'gallery'),
#    (r'^category/artwork/(?P<page_key>[A-Za-z0-9-_/:]+)/$', 'gallery'),
#
#    url(r'^$', admin_views.IndexCtrl.as_django_view(), name=admin_views.IndexCtrl.view_name),    
    
    
)

#urlpatterns += plugin_urls.urlpatterns
