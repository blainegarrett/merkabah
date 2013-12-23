from merkabah.authentication.models import User
class TwitterBackend:
    def authenticate(self, screen_name=None):
        from merkabah.authentication.models import Login
        try:
            login = Login.objects.select_related('user').get(name=screen_name, service_type=Login.TWITTER)
            #if login.user.squelch:
            #    raise Login.DoesNotExist('User banned')
            #login.user.login = login
            return login.user
        except Login.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        return User.objects.get(pk=user_id)