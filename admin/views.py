from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from merkabah.core import controllers as merkabah_controllers
from google.appengine.api import users
from google.appengine.ext import ndb
from django.core import urlresolvers

from plugins.blog import forms as blog_forms
from plugins.blog import models as blog_models

class MerkabahAdminBaseController(merkabah_controllers.MerkabahController):
    chrome_template = 'merkabah/admin/chrome.html'
    require_login = True    
    
class IndexCtrl(MerkabahAdminBaseController):
    view_name = 'merkabah_admin_index'
    template = 'merkabah/admin/index.html'
    

class PluginIndexCtrl(MerkabahAdminBaseController):
    view_name = 'merkabah_admin_plugin_index'
    template = 'merkabah/admin/plugin/index.html'
    
    def process_request(self, request, context, *args, **kwargs):
        context['plugin_key'] = kwargs.get('plugin_key')
        
        context['plugin_base'] = __import__("plugins.%s" % context['plugin_key'], fromlist=["plugins"])
        context['plugin_models'] = __import__("plugins.%s.models" % context['plugin_key'], fromlist=["plugins"])    
        context['plugin_name'] = context['plugin_base'].PLUGIN_NAME
        
        
class PluginKindBaseCtrl(PluginIndexCtrl):
    def process_request(self, request, context, *args, **kwargs):
        super(PluginKindBaseCtrl, self).process_request(request, context, *args, **kwargs)
        context['kind_key'] = kwargs.get('kind_key')

                

class PluginKindIndexCtrl(PluginKindBaseCtrl):
    view_name = 'merkabah_admin_plugin_kind_index'
    template = 'merkabah/admin/plugin/entity/index.html'

    def process_request(self, request, context, *args, **kwargs):
        super(PluginKindIndexCtrl, self).process_request(request, context, *args, **kwargs)
        context['entities'] = context['plugin_models'].get_kind_class(context['kind_key']).query()
        
            
class PluginKindCreateCtrl(PluginKindBaseCtrl):
    view_name = 'merkabah_admin_blog_create'
    template = 'merkabah/admin/plugin/entity/form.html'
    
    def process_request(self, request, context, *args, **kwargs):
        super(PluginKindCreateCtrl, self).process_request(request, context, *args, **kwargs)
        
        context['form_type'] = 'Add'
        
        if request.POST:
            context['form'] = blog_forms.BlogPostForm(request.POST)
            context['form'].is_valid()
            
            if context['form'].is_valid():
                post = blog_models.BlogPost(title=context['form'].cleaned_data['title'], body=context['form'].cleaned_data['body'], slug=context['form'].cleaned_data['slug'])                
                post.put()
                                
                return redirect(urlresolvers.reverse('merkabah_admin_plugin_kind_index', args=(context['plugin_key'], context['kind_key'])))
                            
        else:
            context['form'] = blog_forms.BlogPostForm()
                    
class PluginKindEditCtrl(PluginKindBaseCtrl):
    view_name = 'merkabah_admin_plugin_kind_edit'
    template = 'merkabah/admin/plugin/entity/form.html'
    
    def process_request(self, request, context, *args, **kwargs):
        super(PluginKindEditCtrl, self).process_request(request, context, *args, **kwargs)
        
        context['form_type'] = 'Edit'        
        blog_post_key = ndb.Key(urlsafe=kwargs['entity_key'])
        post = blog_post_key.get()
        
        form_initial = {}
        form_initial['title'] = post.title 
        form_initial['slug'] = post.slug
        form_initial['body'] = post.body
        
        if request.POST:
            context['form'] = blog_forms.BlogPostForm(data=request.POST, initial=form_initial)
            context['form'].is_valid()
        
            if context['form'].is_valid():
                post.title=context['form'].cleaned_data['title']
                post.body=context['form'].cleaned_data['body']
                post.slug=context['form'].cleaned_data['slug']
                post.put()
                
                return redirect(urlresolvers.reverse('merkabah_admin_plugin_kind_index', args=(context['plugin_key'], context['kind_key'])))
                        
        else:
            context['form'] = blog_forms.BlogPostForm(initial=form_initial)
        
        
        
        