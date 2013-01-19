from django.shortcuts import render_to_response
from django.template import Template, Context, RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
import json

import logging
from merkabah.core.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

class MerkabahController(object):
    '''
    Controller Objectives
    - allow interface for all major request types
    - handle ajax responses
    - handle security decorators
    
    - Build a angular controller with the name matching.
    - Provide a list of api methods available
    
    '''
    
    def __init__(self, *args, **kwargs):
        # Store our own name
        self.controller_name = self.__class__.__name__
        
    
    chrome_template = 'base.html'
    require_login = False
    
    method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def process_request(self, request, context, *args, **kwargs):
        """
        method that should be subclassed to process response prior to the
        actual rendering.  This can be used to do any kind of data validation
        and return a response if something doesn't validate.
        """
        return None
        
    @classmethod
    def as_django_view(cls, **initkwargs):
        #@csrf_exempt
        def view(request, *args, **kwargs):
            kwargs['context'] = RequestContext(request, {'context_initialized' : True })
            return cls(**initkwargs).dispatch(request, *args, **kwargs)
        return view
    
    def log_method_not_allowed(self, request):
        raise Exception("%s requests are not allowed for %s" % (request.method.lower(), self))
        
    def method_not_allowed(self, request, *args, **kwargs):
        #logging.error('in method not allowed..')
        self.log_method_not_allowed(request)
        allowed_methods = [m for m in self.method_names if hasattr(self, m)]
        return http.HttpResponseNotAllowed(allowed_methods)
                
    def dispatch(self, request, *args, **kwargs):
        method_name = request.method.lower()
        #logging.error(kwargs)
        #logging.error('hhhhhhhhhhhhhh')
        if method_name in self.method_names:
            handler = getattr(self, method_name, self.method_not_allowed)
        else:
            handler = self.method_not_allowed
        return handler(request, *args, **kwargs)
    
    @login_required
    def render_secure(self, request, context, *args, **kwargs):
        return self.render_html(request, context, *args, **kwargs)
        
    def render_html(self, request, context, *args, **kwargs):
        rendered_content = render_to_string(self.template, context)
        chrome_context = context
        chrome_context.update({'body_content' : rendered_content, 'controller' : self})
        rendered_chrome = render_to_string(self.chrome_template, chrome_context)
        return HttpResponse(rendered_chrome)        
    
    
    def get(self, request, *args, **kwargs):
        #logging.warning('in get...')
        #logging.warning(self.require_login)
        #raise Exception(self.require_login)
        #logging.warning(request.is_ajax())
        #return HttpResponse()
        context = kwargs.pop('context', {})

        # make sure we have enough access for the view
        #reason = self.can_access(context, True)
        #if reason:
        #    return self.access_denied(request, context, reason, *args, **kwargs)
        
        # allow the response to be shortcut before render
        #context['meta'] = self.get_meta(request, context, *args, **kwargs)
        response = self.process_request(request, context, *args, **kwargs)
        if response:
            return response

        # do the html view
        if not request.is_ajax():
            if self.require_login:
                return self.render_secure(request, context, *args, **kwargs)
            else:
                return self.render_html(request, context, *args, **kwargs)

        # do any get request processing
        #logging.warning('still here...')
        response = self.processing_ajax(request, context, *args, **kwargs)
        #logging.error('!?!?!?!??')
        if response:
            return response


        
        # otherwise do the ajax content
        return self.render_ajax(request, context, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        #@self.security_decorator(**self.security_kwargs)
        def secure_post(request, *args, **kwargs):
            context = kwargs.pop('context', {})
            skip = kwargs.pop('skip_process', False)

            # make sure we have enough access for the view
            #reason = self.can_access(context, True)
            #if reason:
            #    return self.access_denied(request, context, reason, *args, **kwargs)
            
            # allow the response to be shortcut before render
            #context['meta'] = self.get_meta(request, context, *args, **kwargs)
            response = self.process_request(request, context, *args, **kwargs)
            if response:
                return response
            
            # do any post request processing
            #if not skip:
            #    response = self.render_processing(request, context, *args, **kwargs)
            #    if response:
            #        return response

            # do the html view
            if not request.is_ajax():
                return self.render_html(request, context, *args, **kwargs)

            # otherwise do the ajax content
            return self.render_ajax(request, context, *args, **kwargs)
        
        # do secure processing
        return secure_post(request, *args, **kwargs)



        
    #@base_decorators.ajax_required
    #@base_decorators.ajax_response    
    def processing_ajax(self, request, context, *args, **kwargs):
        #logging.warning('inside of processing ajax')
        return self.run_processing(request, context, *args, **kwargs)        






     
    def run_processing(self, request, context, *args, **kwargs):
        
        response = None
        if request.method.lower() == 'get':
            request_type = request.GET.get('request_type', None)
            action = request.GET.get('action', None)
        else:
            request_type = request.POST.get('request_type', None)
            action = request.POST.get('action', None)

        #logging.error('----------------%s' % action)
        # handle the incremental or reload update
        #if request_type == 'incremental':
        #    response = self.run_incremental(request, context, *args, **kwargs)
        #    if response:
        #        return response

        # look for a method to handle id + request_type
        '''
        attr = getattr(self, 'process_%s_%s' % (id, request_type), None)
        if attr and callable(attr):
            response = attr(request, context, *args, **kwargs)
            if response:
                return response
        '''

        # look for a method to handle request_type
        attr = getattr(self, 'process_%s' % action, None)
        if attr and callable(attr):
            response = attr(request, context, *args, **kwargs)
            if response:
                return response

        # no response so return the ajax
        return self.get_ajax(request, context, *args, **kwargs)           
    
    def get_ajax(self, request, context, *args, **kwargs):
        rendered_content = render_to_string(self.template, context)
        json_return = json.dumps({'content' : rendered_content, 'controller_name' : self.controller_name})
        return  HttpResponse(json_return)
    
    #######################################################
    # Utility and debug methods 
    #######################################################
    def get_class_name(self):
        return self.__class__.__name__

    def get_class_path(self):
        return self.__class__
        