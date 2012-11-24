# Auth Exceptions

class AuthenticationError(Exception):
    """
    Base exception for all authentication errors.
    """

class AuthenticationRequired(AuthenticationError):
    """
    Base exception for all auth errors.
    """