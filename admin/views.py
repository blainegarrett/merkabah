from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def index(request, page_key=None):
    raise Exception('admin index!')

def homepage(request):
    return render_to_response('homepage.html', RequestContext(request))