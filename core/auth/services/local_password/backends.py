"""
Django authentication backend
"""

from merkabah.core import auth as auth_api
from merkabah.core.auth.services.local_password import check_password


class LocalPasswordAuthenticationBackend(object):
    """
    Django Backend for local password authentication
    """

    def authenticate(self, username=None, password=None):
        user = auth_api.get_user_by_username(username)
        if not user:
            return None

        login = auth_api.get_login_by_user_and_type(user, 'password')

        if not login:
            return None

        # Validate here
        if (password is not None and check_password(password, login)):
            setattr(user, 'USED_LOGIN', login)
            return user
