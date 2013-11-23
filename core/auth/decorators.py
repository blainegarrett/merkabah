import logging
from merkabah.core import decorators
from merkabah.core.auth import AuthenticationRequired
from google.appengine.api import users as gusers
from django.http import HttpResponseRedirect

import logging

class LoginRequired(object):
    """
    tail_recursive decorator based on Kay Schluehr's recipe
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/496691
    with improvements by me and George Sakkis.
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwd):

        
        # TODO: urlescape the return path, etc
        return_url = args[0].META['PATH_INFO'] + '?'+ args[0].META['QUERY_STRING']

        guser = gusers.get_current_user()
        
        if not guser:
            logging.warning('Unauthenicated user attempted to accesss this url.')
            return HttpResponseRedirect(gusers.create_login_url(return_url))

        # They are authenticated...

        email = guser.email()
        if not email == 'blaine@blainegarrett.com':
            logging.debug('Loading request for authenticated user %s.' % guser.email())
            return HttpResponseRedirect('/?login=unauthenticated')

        return self.func(*args, **kwd)
        

class NoLogin(object):
    """
    tail_recursive decorator based on Kay Schluehr's recipe
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/496691
    with improvements by me and George Sakkis.
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwd):
        return self.func(*args, **kwd)

def nologin_required(ctrl, f, *args, **kwargs):
    """
    Simple Decorator to not login
    """
    return decorators.decorator_apply(NoLogin, f)


def login_required(ctrl, f, *args, **kwargs):
    """
    Simple Decorator to login
    """
    return decorators.decorator_apply(LoginRequired, f)

    
'''
class login_required(BaseDecorator):
    """
    Provides an easy way to ensure that the user has already logged on. Only
    the existance of the C{user} key in the session is checked.

    Useful for decorating service methods. If the request is not authenticated
    then L{auth.AuthorizationRequired} is raised.
    """

    def init(self, *args, **kwargs):
        BaseDecorator.init(self, *args, **kwargs)

        self.will_raise(auth.AuthorizationRequired)
        self.will_raise(auth.LoggedOut)

    def call(self, request, *args, **kwargs):
        session = request.session

        if 'user' not in session:
            logging.info('missing `user` in session %r', session.session_key)

            raise auth.AuthorizationRequired

        if session['user'] is None:
            raise auth.LoggedOut

        if session['user'].suspended:
            raise auth.AuthorizationRequired('User is suspended')

        return BaseDecorator.call(self, request, *args, **kwargs)
'''   