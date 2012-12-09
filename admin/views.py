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