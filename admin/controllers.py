from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from merkabah.core import controllers as merkabah_controllers
from google.appengine.api import users
from google.appengine.ext import ndb
from django.core import urlresolvers
from google.appengine.api import users as gusers
import settings
from django.http import HttpResponse, HttpResponseNotAllowed

#from plugins.blog import forms as blog_forms
#from plugins.blog import models as blog_models

class PluginLoadingFailed(Exception):
    pass

class MerkabahAdminBaseController(merkabah_controllers.MerkabahController):
    chrome_template = 'merkabah/admin/chrome.html'
    require_login = True    

    def process_request(self, request, context, *args, **kwargs):
        """
        Populate a set of primary menu options for the whole of the admin
        """
        context['primary_menu'] = settings.ADMIN_PRIMARY_MENU
        
        # TODO: This should be done in the middleware...
        guser = gusers.get_current_user()
        context['user'] = guser

    def process_yodal(self, request, context, *args, **kwargs):
        return merkabah_controllers.RedirectResponse('http://google.com')

    def process_fart(self, request, context, *args, **kwargs):
        return merkabah_controllers.AlertResponse(request.POST['squirel'])
    
    def process_dialog_yo(self, request, context, *args, **kwargs):
        return merkabah_controllers.DialogResponse('Pork', 'Katie is so cool')

    def process_error_display(self, request, context, *args, **kwargs):
        return merkabah_controllers.ErrorResponse('Your shit is fucked')

    def process_throw_exception(self, request, context, *args, **kwargs):
        raise Exception('This is not working...')

class IndexCtrl(MerkabahAdminBaseController):
    view_name = 'merkabah_admin_index'
    template = 'merkabah/admin/index.html'

###########################
# Plugin Response Types
###########################
class BasePluginResponse(object):
    pass

class TemplateResponse(BasePluginResponse):
    def __init__(self, plugin, template, context):
        self.plugin = plugin
        self.template = template
        self.context = context

    def unicode(self):
        return self.__str__

    def __str__(self):
        from django.template.loader import render_to_string
        self.context['plugin'] = self.plugin
        return render_to_string(self.template, self.context)

###########################
# Plugin Hanlders
##########################

class PluginBaseCtrl(MerkabahAdminBaseController):
    def load_plugin(self, plugin_slug, request, context, *args, **kwargs):
        """
        """
        import importlib


        # Step 1: Check if plugin exists in list of installed plugsin
        if not context['plugin_slug'] in settings.INSTALLED_PLUGINS:
            raise PluginLoadingFailed('Plugin "%s" is not in settings.INSTALLED_PLUGINS' % context['plugin_slug'])
        
        # Step 2: import module
        try:
            plugin_module = importlib.import_module('plugins.%s' % plugin_slug)
        except ImportError, e:
            raise PluginLoadingFailed('Unable to import %s plugin module. Please install module at /plugins/%s' % (plugin_slug,plugin_slug))

        # Step 3: Determine Action
        action = kwargs.pop('action', 'index')

        # Step 4: Determine Plugin Class
        pluginClass = plugin_module.pluginClass
        
        p = pluginClass()

        action_method_name = 'process_%s' % action
        
        if not hasattr(p, action_method_name):
            raise PluginLoadingFailed('Plugin module %s does not have method %s' % (p, action_method_name))
        
        action_method = getattr(p, action_method_name)
        if not callable(action_method):
            raise PluginLoadingFailed('Plugin module %s does not have callable method %s' % (p, action_method_name))

        # Process response...
        result = action_method(request, context, *args, **kwargs)

        #if isinstance(result, basestring) or isinstance(result, TemplateResponse):
        #    context['plugin_content'] = result
        #    return
        #raise Exception('Plugin result is of type %s', type(result))
        context['plugin_content'] = result

    def process_request(self, request, context, *args, **kwargs):
        """
        Plugin Loader
        """
        super(PluginBaseCtrl, self).process_request(request, context, *args, **kwargs)

        context['plugin_slug'] = kwargs.pop('plugin_slug')
        
        try:
            self.load_plugin(context['plugin_slug'], request, context, *args, **kwargs)
        except PluginLoadingFailed, e:
            context['error'] = str(e)

class PluginIndexCtrl(PluginBaseCtrl):
    view_name = 'admin_plugin_index'
    template = 'merkabah/admin/plugin_index.html'


class PluginActionCtrl(PluginBaseCtrl):
    view_name = 'admin_plugin_action'
    template = 'merkabah/admin/plugin_index.html'



        
        
        