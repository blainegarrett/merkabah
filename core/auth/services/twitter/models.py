from merkabah.authentication.models import PendingUser, Login, User
class TwitterPendingUser(PendingUser):
    site_desc = u'Twitter'
    auth_type = Login.TWITTER
    auth_key = 'screen_name'

    def __init__(self, screen_name, access_token_str, userinfo):
        self.userinfo = userinfo        
        self.username = screen_name
        self.full_name = self.userinfo.name
        self.login_key = access_token_str
        
    def get_default_username(self):
        return self.username
        
    def get_default_email(self):
        return ''

    
    def get_authentication_credentials_dict(self):
        return {'screen_name' : self.username, } #access_token_str
        
    def create_account(self):
        # first trying signing in as-is
        user = authenticate(screen_name=self.username)
        if user:
            return user
        
        import random

        email = self.get_default_email()

        # next, see if there is an account with the same e-mail
        #try:
        #    user = User.objects.get(email=email)
        #except User.DoesNotExist:
        #    user = None
        
        # try creating a user.  append a suffix if there is a collision
        suffix = ''
        attempts = 100
        while not user:
            attempts -= 1    
            try:
                user = User.objects.create_user(self.alias + suffix, self.get_default_email(), confirmed=True)
            except IntegrityError, e:
                if attempts <= 0:
                    raise
                suffix = '-%02d' % random.randint(1,99)

        # there shouldn't be an IntegrityError by this point, but just to be sure...
        if True: #try:
            login = Login.objects.create(
                user=user,
                name=self.username,
                service_type=Login.TWITTER,
                key = self.access_token_str
            )
        #except IntegrityError, e:
        #    pass
        
        return authenticate(sn=self.alias)
    
    def send_create_email(self, user, request):
        return None
    
    def send_new_user_notice_email(self, user, request):
        pass
        #from helpers.twitter import send_twitter_event_notice_to_feedback
        # Send a notice to feedback 
        #send_twitter_event_notice_to_feedback(request, 3, self.alias, {'user' : user})