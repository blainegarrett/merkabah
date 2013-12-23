"""
Merkabah's django authentication backend
"""
from merkabah.core import auth as auth_api

class LocalPasswordAuthenticationBackend(object):
    """
    
    """
    def authenticate(self, username=None, password=None):
        """
        """

        try:
            user = auth_api.get_user_by_username(username)
            if not user:
                return None
            login = auth_api.get_login_by_user_and_type(user, 'password')

            if not login:
                return None

            # Validate here
            if (password is not None and login.check_password(password)):
                setattr(user, 'USED_LOGIN', login)
                #login.user.login = login # user.login is "dynamic" strictly in memory reference for the current login for the user.
                return user

        except Exception, e: #Login.DoesNotExist:
            raise Exception(e) #TODO: This could/should/would return None. Eventually do this when we get out of beta        

    def get_user(self, user_id):
        from merkabah.authentication import cache as user_cache 
        return user_cache.get_by_id(user_id)