"""
Core Auth Models
"""
from google.appengine.ext import ndb


class Account(ndb.Model):
    """
    Merkabah Base Account to group Users by
    """

    account_name = ndb.StringProperty()
    account_id = ndb.StringProperty()


class User(ndb.Model):
    """
    """

    username = ndb.StringProperty()
    email = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()


class AnonymousUser(object):
    id = None
    pk = None
    def __init__(self):
        pass
    def __unicode__(self):
        return 'AnonymousUser'
    def __str__(self):
        return unicode(self).encode('utf-8')
    def __eq__(self, other):
        return isinstance(other, self.__class__)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return 1 # instances always return the same hash value
    def save(self):
        raise NotImplementedError
    def delete(self):
        raise NotImplementedError
    def get_and_delete_messages(self):
        return []
    def is_anonymous(self):
        return True
    def is_pending(self):
        return False
    def is_authenticated(self):
        return False


class Membership(ndb.Model):
    """
    """
    user_key = ndb.KeyProperty(kind=User)
    account_key = ndb.KeyProperty(kind=Account)

    @property
    def user(self):
        if not self._user:
            self._user = self.user_key.get()
        return self.user

    @property
    def account(self):
        if not self._account:
            self._account = self.account_key.get()
        return self._user


class Login(ndb.Model):
    """
    Note: These have a EG parent of a user and the keys are in the form of
    ndb.Key('User', id, 'Login',)
    
    """

    auth_type = ndb.StringProperty()
    auth_token = ndb.StringProperty()
    auth_data = ndb.StringProperty()
    user_key = ndb.KeyProperty(kind=User)

    @property
    def user(self):
        if not self._user:
            self._user = self.user_key.get()
        return self.user
    
    @staticmethod
    def generate_key_name(user, auth_type):
        # TODO: Check for valid auth_type
        # TODO: Check arg types
        # TODO: This auth_type_should probably be an int
        return "%s:%s" % (user.key.id(), auth_type)
    
    @staticmethod
    def generate_key(user, auth_type):
        l_key = ndb.Key('Login', Login.generate_key_name(user, auth_type), parent=user.key)
        return l_key

    def check_password(self, password):
        if not self.auth_type == 'password':
            return False
        
        if password == self.auth_token:
            return True

        return False


    #password
    #twitter
    #facebook
    #google
    #openid


class Permission(ndb.Model):
    """
    """


class UserPermission(ndb.Model):
    """
    """


class UserPreference(ndb.Model):
    """
    """
