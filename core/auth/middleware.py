# Borrowed (heavily) from django.contrib.auth
class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            from merkabah.authentication import get_user
            request._cached_user = get_user(request)
        return request._cached_user

class AuthenticationMiddleware(object):
    def process_request(self, request):
        from merkabah.core.auth import get_user

        request._cached_user = get_user(request)
        ##request.__class__.user = LazyUser()
        return None
