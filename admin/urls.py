"""
Merkabah Admin Urls
"""
from django.conf.urls.defaults import patterns, url
from merkabah.admin import controllers as ac

urlpatterns = patterns('merkabah.admin.views',

    # Main index of the admin controller
    url(r'^$', *ac.IndexCtrl.django_url_args()),

    # Plugin Controller Endpoints
    url(r'^plugin/(?P<plugin_slug>[A-Za-z0-9-_]+)/$', *ac.PluginIndexCtrl.django_url_args()),
    url(r'^plugin/(?P<plugin_slug>[A-Za-z0-9-_]+)/(?P<action>[A-Za-z0-9-_]+)/$', *ac.PluginActionCtrl.django_url_args()),


#    url(r'^plugin/(?P<plugin>[A-Za-z0-9-_/:]+)/$', *admin_views.PluginCtrl.django_url_args()),   
#    (r'^gallery/(?P<page_key>[A-Za-z0-9-_/:]+)/$', 'gallery'),
#    (r'^category/artwork/(?P<page_key>[A-Za-z0-9-_/:]+)/$', 'gallery'),
#
#    url(r'^$', *admin_views.IndexCtrl.django_url_args()),    
    
    
)

#urlpatterns += plugin_urls.urlpatterns
