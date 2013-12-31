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

# Exceptions
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


class IndexCtrl(MerkabahAdminBaseController):
    """
    Index Controller for whole of admin.

    TODO: This is slated to be a customizable admin dashboard
    """

    view_name = 'merkabah_admin_index'
    template = 'merkabah/admin/index.html'


###########################
# Plugin Framework Controllers
##########################
class PluginBaseCtrl(MerkabahAdminBaseController):
    """
    Base Controller for All Plugin Administration Behavior
    """

    def load_plugin(self, plugin_slug, request, context, *args, **kwargs):
        """
        Given a plugin slug, attempt to load it and then process the request
        """

        import importlib

        # Step 1: Check if plugin exists in list of installed plugsin
        if not plugin_slug in settings.INSTALLED_PLUGINS:
            m = 'Plugin "%s" is not in settings.INSTALLED_PLUGINS'
            raise PluginLoadingFailed(m % plugin_slug)
        
        # Step 2: import module
        try:
            plugin_module = importlib.import_module('plugins.%s' % plugin_slug)
        except ImportError, e:
            m = 'Unable to import %s plugin module. Please install module at /plugins/%s'
            raise PluginLoadingFailed(m % (plugin_slug, plugin_slug))

        # Step 3: Determine Action
        # TODO: This should be reworked more
        action = kwargs.pop('action', 'index')

        # Step 4: Determine Plugin Class
        pluginClass = plugin_module.pluginClass

        p = pluginClass()

        action_method_name = 'process_%s' % action

        if not hasattr(p, action_method_name):
            'Plugin module %s does not have method %s'
            raise PluginLoadingFailed(m % (p, action_method_name))

        action_method = getattr(p, action_method_name)
        if not callable(action_method):
            m = 'Plugin module %s does not have callable method %s'
            raise PluginLoadingFailed(m % (p, action_method_name))

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

        # response could be nearly anything that can be handled by the merkabah framekwork

        return response


class PluginIndexCtrl(PluginBaseCtrl):
    """
    Plugin BaseCtrl
    TODO: This seems like we could get rid of this
    """

    view_name = 'admin_plugin_index'
    #template = 'merkabah/admin/plugin_index.html'


class PluginActionCtrl(PluginBaseCtrl):
    view_name = 'admin_plugin_action'
    #template = 'merkabah/admin/plugin_index.html'


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
