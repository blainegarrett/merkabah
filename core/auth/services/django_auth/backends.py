# This is a wrapper for the django authentication backend. 
# It adds support and hooks for merkabah features to the native django authentication system
from django.contrib.auth.backends import ModelBackend
class DjangoAuthenticationBackend(object):
    def authenticate(self, username=None, password=None):
        auth_method = ModelBackend()
        user = auth_method.authenticate(username, password)
        
        if True: # settings.ENABLE_LOGIN_TYPES
            pass
        return user
    
    def get_user(self, user_id):
        auth_method = ModelBackend()
        user = auth_method.get_user(user_id)
        #TODO: Add merkabah security hooks Check ban status, ipbans, etc
        return user