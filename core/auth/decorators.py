import logging
from merkabah.core import decorators
from merkabah.core.auth import AuthenticationRequired
from google.appengine.api import users as gusers
from django.http import HttpResponseRedirect

@decorators.decorator
def login_required(f, *args, **kwargs):
    """
    Simple Decorator to require login
    """
    # TODO: urlescape the return path, etc
    return_url = args[1].META['PATH_INFO'] + '?'+ args[1].META['QUERY_STRING']

    guser = gusers.get_current_user()

    if not guser:
        return HttpResponseRedirect(gusers.create_login_url(return_url))
        #raise AuthenticationRequired('Could not retrieve a Google User. Please Login. ')
    
    return f(*args, **kwargs)

    
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