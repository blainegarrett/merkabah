"""
A collection of controllers used for administration of the the Merkabah install
"""

#from django.shortcuts import render_to_response
#from django.shortcuts import redirect
#from django.template import RequestContext
from merkabah.core.controllers import MerkabahDjangoController
from merkabah.core.auth.decorators import login_required

from merkabah.core import controllers as merkabah_controllers
from merkabah.core import auth as auth_api
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


#from google.appengine.api import users
#from google.appengine.ext import ndb
#from django.core import urlresolvers

import settings
#from django.http import HttpResponse, HttpResponseNotAllowed


class PluginLoadingFailed(Exception):
    pass

class MerkabahAdminBaseController(MerkabahDjangoController):
    """
    Base Controller for Merkabah Admin panel

    """

    chrome_template = 'merkabah/admin/chrome.html'
    require_login = True
    auth_decorator = login_required

    def process_request(self, request, context, *args, **kwargs):
        """
        Populate a set of primary menu options for the whole of the admin
        """
        context['primary_menu'] = settings.ADMIN_PRIMARY_MENU

    def process_yodal(self, request, context, *args, **kwargs):
        return merkabah_controllers.RedirectResponse('http://google.com')

    def process_fart(self, request, context, *args, **kwargs):
        return (merkabah_controllers.AlertResponse('One chained alert.'), merkabah_controllers.AlertResponse('Two chained alert.'))

    def process_dialog_yo(self, request, context, *args, **kwargs):
        return merkabah_controllers.DialogResponse('Pork', 'Katie is so cool')

    def process_error_display(self, request, context, *args, **kwargs):
        return merkabah_controllers.ErrorResponse('Your shit is fucked')

    def process_throw_exception(self, request, context, *args, **kwargs):
        raise Exception('This is not working...')
    
    def process_load_content(self, request, context, *args, **kwargs):
        return merkabah_controllers.ContentResponse('My favorite color is <span id="dyn_color">green</span>. <a class="btn btn-primary action" href="/madmin/?action=load_content2&amp;node_id=dyn_color"><span class="btn-icon icon-user"></span><span class="btn-text">Make Red</span></a>', request.GET['node_id'])

    def process_load_content2(self, request, context, *args, **kwargs):
        return merkabah_controllers.ContentResponse('red', request.GET['node_id'])

class IndexCtrl(MerkabahAdminBaseController):
    view_name = 'merkabah_admin_index'
    template = 'merkabah/admin/index.html'


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

        return result

    def process_request(self, request, context, *args, **kwargs):
        """
        Plugin Loader
        """

        super(PluginBaseCtrl, self).process_request(request, context, *args, **kwargs)

        context['plugin_slug'] = kwargs.pop('plugin_slug')

        try:
            response = self.load_plugin(context['plugin_slug'], request, context, *args, **kwargs)
        except PluginLoadingFailed, e:
            # Return response...
            context['error'] = str(e)
            return 

        #raise Exception(type(result))
        return response


class PluginIndexCtrl(PluginBaseCtrl):
    view_name = 'admin_plugin_index'
    template = 'merkabah/admin/plugin_index.html'


class PluginActionCtrl(PluginBaseCtrl):
    view_name = 'admin_plugin_action'
    template = 'merkabah/admin/plugin_index.html'


class AuthLoginCtrl(MerkabahDjangoController):
    chrome_template = 'merkabah/admin/chrome.html'
    require_login = False
    template = 'merkabah/admin/login.html'
    view_name = 'cmd_auth_login'

    def process_request(self, request, context, *args, **kwargs):

        context['return_url'] = request.REQUEST.get('return_url', '/') # DEFAULT LANDING PAGE
        if request.POST:

            username = request.POST['username']
            password = request.POST['password']

            # Step 2: Authenticate User from un/pw authentication methods
            user = auth_api.authenticate(username=username, password=password)

            if user:
                auth_api.login(request, user, user.USED_LOGIN)

                redirect_url = '/' # DEFAULT LANDING PAGE
                if 'return_url' in request.POST:
                    redirect_url = request.POST.get('return_url')

                if not redirect_url:
                    redirect_url = '/' # DEFAULT LANDING PAGE
                return HttpResponseRedirect(redirect_url)
            else:
                context['error'] = 'Username/Password combo does not exist.'


class AuthLogoutCtrl(MerkabahDjangoController):
    chrome_template = 'merkabah/admin/chrome.html'
    require_login = False
    view_name = 'cmd_auth_logout'

    def process_request(self, request, context, *args, **kwargs):
        auth_api.logout(request)
        return HttpResponseRedirect(reverse('cmd_auth_login'))
