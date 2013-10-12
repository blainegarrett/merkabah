"""
.. module:: merkabah.core.controllers
   :synopsis: Contains classes for controllers

.. moduleauthor:: Blaine Garrett <blaine@blainegarrett.com>

"""

import json

from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse

from merkabah.core.auth.decorators import nologin_required


class BaseResponse(object):
    """
    Base Response Class for all response types
    """

    def __init__(self, *args, **kwargs):
        """

        """
        self.response_dict = {}

    def get_response(self):
        """
        """

        self.response_dict = {'response_type': self.response_type}
        self.populate_response()
        return json.dumps(self.response_dict)


class AlertResponse(BaseResponse):
    """
    Respose to alert some text
    """

    response_type = 'alert'

    def __init__(self, *args, **kwargs):
        self.message = args[0]

    def populate_response(self):
        self.response_dict['message'] = self.message


class ErrorResponse(BaseResponse):
    response_type = 'error'

    def __init__(self, *args, **kwargs):
        self.content = args[0]

    def populate_response(self):
        self.response_dict['content'] = self.content


class RedirectResponse(BaseResponse):
    response_type = 'redirect'

    def __init__(self, *args, **kwargs):
        self.url = args[0]

    def populate_response(self):
        self.response_dict['url'] = self.url


class CloseFormResponse(BaseResponse):
    response_type = 'close_form_dialog'

    def __init__(self, id):
        self.id = id

    def populate_response(self):
        self.response_dict['form_id'] = self.id


class DialogResponse(BaseResponse):
    response_type = 'dialog'

    def __init__(self, title, content, *args, **kwargs):
        self.title = title
        self.content = content

    def populate_response(self):
        self.response_dict['content'] = self.content
        self.response_dict['title'] = self.title


class FormResponse(BaseResponse):
    response_type = 'form'

    def __init__(self, form, id, title, target_url, target_action):
        self.form = form
        self.id = id
        self.title = title
        self.target_url = target_url
        self.target_action = target_action

    def populate_response(self):
        self.response_dict['form'] = self.form.as_bootstrap()
        self.response_dict['form_id'] = self.id
        self.response_dict['title'] = self.title
        self.response_dict['target_url'] = self.target_url
        self.response_dict['target_action'] = self.target_action


class FormDialogResponse(BaseResponse):
    response_type = 'form_dialog'

    def __init__(self, title, content, *args, **kwargs):
        self.title = title
        self.content = content

    def populate_response(self):
        self.response_dict['content'] = self.content
        self.response_dict['title'] = self.title


class ContentResponse(BaseResponse):
    response_type = 'dynamic_content'

    def __init__(self, content, id):
        self.content = content
        self.node_id = id

    def populate_response(self):
        self.response_dict['content'] = self.content
        self.response_dict['node_id'] = self.node_id


class TemplateResponse(BaseResponse):
    response_type = 'template'

    def __init__(self, template, context):
        self.template = template
        self.context = context

    def unicode(self):
        return self.__str__()

    def __str__(self):
        result = render_to_string(self.template, self.context)
        return result

    def populate_response(self):
        self.response_dict['content'] = self.unicode()


class FormErrorResponse(BaseResponse):
    response_type = 'form_error'

    def __init__(self, form, id):
        self.form = form
        self.id = id

    def populate_response(self):
        import json

        self.response_dict['form_id'] = self.id
        self.response_dict['form_errors'] = json.dumps(self.form.errors)


class MerkabahController(object):
    """
    Controller Objectives
    - allow interface for all major request types
    - handle ajax responses
    - handle security decorators
    - Build a angular controller with the name matching.
    - Provide a list of api methods available
    """

    chrome_template = 'base.html'
    require_login = False
    auth_decorator = nologin_required
    content_title = ''
    method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def __init__(self, *args, **kwargs):
        # Store our own name
        self.controller_name = self.__class__.__name__

    def process_request(self, request, context, *args, **kwargs):
        """
        method that should be subclassed to process response prior to the
        actual rendering.  This can be used to do any kind of data validation
        and return a response if something doesn't validate.
        """
        return None

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch method called via your implementation (django) etc of the "view"
        Note: context will be a kwarg
        """

        @self.auth_decorator
        def authenticated_dispatch(request, *args, **kwargs):
            return self._dispatch(request, *args, **kwargs)

        if self.auth_decorator and callable(self.auth_decorator):
            return authenticated_dispatch(request, *args, **kwargs)
        else:
            return self._dispatch(request, *args, **kwargs)

    def _dispatch(self, request, *args, **kwargs):
        """
        Dynamic handler... routes all allowed request types through here

        This returns a valid HttpRespponse
        """

        context = kwargs.pop('context', {})

        # Check process response

        response = self.process_request(request, context, *args, **kwargs)

        # If it is a template response and it is not ajax, render it as a content body
        #   it is likely a angular template url or a redrect, etc.

        if response:
            if isinstance(response, TemplateResponse):
                # TODO: REFACTOR THIS
                rendered_content = unicode(response)

                chrome_context = context
                chrome_context.update({'content_title': self.content_title,
                                        'body_content': rendered_content,
                                        'controller': self})
                rendered_chrome = render_to_string(self.chrome_template, chrome_context)
                return HttpResponse(rendered_chrome)

            else:
                return self.action_response_helper(response)

        # Action based Responses
        action = request.REQUEST.get('action', None)
        if not action:
            action = context.get('action', None)

        # There is an action to evaluate
        if action:
            attr = getattr(self, 'process_%s' % action, None)
            if attr and callable(attr):
                response = attr(request, context, *args, **kwargs)
            else:
                raise Exception('Attempting to evaluate method %s' % action)

        # If not ajax - just render the output
        if not response and not request.is_ajax():
            return self.render_html(request, context, *args, **kwargs)

        if not response:
            response = self.processing_ajax(request, context, *args, **kwargs)

        # If it is an instance of
        if response:
            return self.action_response_helper(response)

    def action_response_helper(self, response):
        if isinstance(response, (BaseResponse, list, tuple)):
            if not isinstance(response, (list, tuple)):
                responses = [response]
            else:
                responses = response

            return_response_list = []
            for r in responses:
                return_response_list.append(r.get_response())
            return HttpResponse(json.dumps({'action_response_list': return_response_list}))

    def render_html(self, request, context, *args, **kwargs):
        """
        Render the HTML
        """
        rendered_content = render_to_string(self.template, context)
        chrome_context = context
        chrome_context.update({'content_title': self.content_title,
            'body_content': rendered_content,
            'controller': self})
        rendered_chrome = render_to_string(self.chrome_template, chrome_context)
        return HttpResponse(rendered_chrome)


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
            #request_type = request.POST.get('request_type', None)
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
        else:
            # Not an action call
            response = self.get_ajax(request, context, *args, **kwargs)

        return response

    def get_ajax(self, request, context, *args, **kwargs):
        rendered_content = render_to_string(self.template, context)
        json_return = json.dumps({'content': rendered_content,
                                    'controller_name': self.controller_name})
        return  HttpResponse(json_return)

    #######################################################
    # Utility and debug methods
    #######################################################

    def get_class_name(self):
        return self.__class__.__name__

    def get_class_path(self):
        return self.__class__


class MerkabahDjangoController(MerkabahController):
    """
    Wrapper Class for Django Implementation
    """

    @classmethod
    def as_django_view(cls, **initkwargs):
        """
        Generates a django view container for controller.
        This is useful when using django urls.
        """

        def view(request, *args, **kwargs):
            kwargs['context'] = RequestContext(request, {'context_initialized': True})
            return cls(**initkwargs).dispatch(request, *args, **kwargs)
        return view

    @classmethod
    def django_url_args(cls, **initkwargs):
        """
        Return a tuple of django url args
        """
        django_kwargs = {'name': cls.view_name}
        return (cls.as_django_view(), django_kwargs)
