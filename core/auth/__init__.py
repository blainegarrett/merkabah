# Auth Exceptions
from merkabah.core.auth import models as auth_models
from merkabah.core.entities import log_event
from django.contrib import auth as django_auth
from google.appengine.ext import ndb

# Authentication Interfaces
def authenticate(**credentials):
    return django_auth.authenticate(**credentials)

SESSION_KEY = 'merkabah_SESSID'

def login(request, user, login_obj):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request.
    """

    if user is None:
        user = request.user

    try:
        request.session[SESSION_KEY] = user.key.id()
    except(AttributeError):
        raise Exception('Session Middleware is not installed or not working')

    # TODO: Fire of login event
    request.user = user

def logout(request):
    request.session.terminate()
    if hasattr(request, 'user'):
        del request.user
    if hasattr(request, '_cached_user'):
        del request._cached_user

def get_user(request):
    from merkabah.core.auth.models import User, AnonymousUser
    user = AnonymousUser()

    if request.session.get(SESSION_KEY, None):
        user_key_name = request.session[SESSION_KEY]

        if user_key_name:
            user = ndb.Key('User', user_key_name).get()

    # Do additional checks here for IPbans, user bans, etc        
    if not user:
        user = AnonymousUser()    
    try:
        pass
    except:
        return AnonymousUser()
    return user


def get_user_by_username(username):
    # TODO: Normalize username
    return auth_models.User.query().filter(auth_models.User.username == username).get()


def get_login_by_user_and_type(user, auth_type):
    l_key = auth_models.Login.generate_key(user, auth_type)

    login = l_key.get()
    return login














class AuthenticationError(Exception):
    """
    Base exception for all authentication errors.
    """


class AuthenticationRequired(AuthenticationError):
    """
    Base exception for all auth errors.
    """

# Accounts


def create_account(account_name, account_number, creator=None):
    a = auth_models.Account(account_name=account_name, account_id=account_number)
    a_key = a.put()

    log_event('account_created', a_key, creator)
    return a_key


# Users
def get_users(cursor=None):
    """
    Fetch a paginated list of users
    """
    q = auth_models.User.query()
    return q.fetch()
    

def create_user(username, email, first_name, last_name, creator=None):
    u = auth_models.User(username=username,
                         email=email,
                         first_name=first_name,
                         last_name=last_name)
    u_key = u.put()

    log_event('user_created', u_key, creator)
    return u_key


def get_logins(user):
    q = auth_models.Login.query()
    q.filter(auth_models.Login.user_key == user.key)

    return q.fetch()


def create_login(user, auth_type, auth_token, auth_data, creator=None):
    l_key = auth_models.Login.generate_key(user, auth_type)

    l = auth_models.Login(key=l_key)

    l.auth_type = auth_type
    l.auth_token = auth_token
    l.auth_data = auth_data
    l.user_key = user.key

    l_key = l.put()
    log_event('login_added', l_key, creator)

    return l_key


def create_membership(user, account, creator=None):
    m = auth_models.Membership()

    m.user_key = user.key
    m.account_key = account.key
    m_key = m.put()

    log_event('membership_added', m_key, creator)
    return m_key
