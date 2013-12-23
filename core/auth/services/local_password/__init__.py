from merkabah.core.auth.models import User, Login
#from merkabah.authentication.helpers import hash_email
import datetime

# Not currently in use, but probably should be the only way to create a user
# Wrap in transaction
def register_user(username, email, confirmed=False):
    raise Exception('Not currently in use!!! See merkabah.authentication.services.local_password.__init__.py')
    email_hash = hash_email(email)
    confirmation_key = 'sdfsdfsdfsdfsdfsdfsdf'
    squelch_value = 0
    user = User(username=username, email=email, email_hash=email_hash, created=datetime.datetime.now(), confirmed=confirmed, confirmation_key=confirmation_key, squelch = squelch_value) #TODO:DEFAULT
    user.save()
    return user