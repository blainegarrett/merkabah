#TODO: Lazy Load all this stuff
from merkabah.authentication.forms import BaseMerkabahRegistrationForm, BaseMerkabahLoginForm    
from django import forms
from merkabah.authentication.models import User, Login
from merkabah.authentication.helpers import random_password
from merkabah import authentication as auth

class BaseAccountRegistrationForm(BaseMerkabahRegistrationForm):
    email = forms.EmailField()
    
    #Validation Methods
    #def clean_email(self):    
    #    #try:
    #    #    user = User.objects.get(email__iexact=self.cleaned_data['email'])
    #    #    raise forms.ValidationError('The e-mail address you entered is already in use on our site by another member.')
    #    #except User.DoesNotExist:                    
    #    #    pass
    #    #    #TODO: Check for domain bans on email address setting...
    #
    #def clean(self):
    #    #if not self._errors:
    #    #    self.clean_email()
    #    return super(BaseMerkabahRegistrationForm, self).clean()        
        

class LocalPasswordRegistrationForm(BaseAccountRegistrationForm):
    username = forms.CharField()    
    def clean(self):
        if not self._errors:
            try:
                u = User.objects.get(username__iexact=self.cleaned_data['username'])
                raise forms.ValidationError('The member name you have chosen is already in use.')
            except User.DoesNotExist:
                pass    
        return super(BaseAccountRegistrationForm, self).clean()
    
    def save(self):
        from merkabah.authentication.services.local_password import register_user
        if not self.cleaned_data or self._errors:
            raise Exception()
        
        # Create the User
        user = register_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'])
        
        # Create the localPassword Login Object
        login = Login(user=user, name=user.username, service_type=Login.LOCAL)
        password = random_password(5,5)
        login.set_password(password)
        login.save()
        user.login = login
        #data['user'] = user
        #do_login(request, login)
        
        return user
        
class CreateAccountForm(LocalPasswordRegistrationForm):
    '''This form is used when a new OpenID user chooses to create an
        account after the first successful authentication of a new
        OpenID.  When you call is_valid(), the form will check to make
        sure the account (alias and password) does not yet exist, and if not, it
        will create the User account and return the new account in
        cleaned_data['user'].

        Note: the calling view is responsible for creating the new
        Login and linking it to the user in cleaned_data['user'] because
        only the view knows about the OpenID.'''
    member_name = forms.RegexField(
        r'^[\w-]+$',
        label=u'Choose a Member name',
        max_length=255,
        widget=forms.TextInput(attrs={'class':'txt50'}),
        error_message=u'Please use only letters (a-z), numbers (0-9), underscore (_), and hyphen (-)', 
    )
    #return super(CreateAccountForm, self).clean()


class AssociateAccountForm(forms.Form): #TODO SigninForm
    '''This form is used when a new OpenID user chooses to associate
        his or her OpenID with an existing Propeller local account after
        the first successful authentication of a new OpenID.  When you
        call is_valid(), the form will check to make sure the supplied
        member_name and password map to a valid User account.  If so,
        the existing account is returned in cleaned_data['user'].

        Note: The calling view is responsible for creating the new
        Login and linking it to the existing account because only
        the view knows about the OpenID.'''
    member_name = forms.CharField()
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    def clean(self):
        if not self._errors:
            user = auth.authenticate(username=self.cleaned_data['member_name'], password=self.cleaned_data['password'])
            if not user:
                raise forms.ValidationError('No account can be found with the member name and password supplied.')
            self.cleaned_data['user'] = user
        return super(AssociateAccountForm, self).clean()
        
#TODO: Convert this to LoginLocalAccount
class SigninLocalAccount(BaseMerkabahLoginForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    def render_simple_form(self):
        from merkabah.library.view_tools import render_to_string
        context = {'form' : self }
        template = 'authentication/services/local_password/simple_login_form.html'
        return render_to_string(template, context)
        
    #def __init__(self, *args, **kwargs):
    #    super(SigninLocalAccount, self).__init__(*args, **kwargs)
    #    self.fields['password'].help_text = _('<a href="%s">Forgot your password?</a>') % reverse('security.views.forgot')
    #
    #def clean(self):
    #    if not self._errors:
    #        user = authenticate(alias=self.cleaned_data['member_name'], password=self.cleaned_data['password'])
    #        if not user:
    #            raise forms.ValidationError('Invalid member name or password.')
    #        if not user.confirmed:
    #            raise forms.ValidationError('This account is not yet activated.  Please click the activation link in the e-mail we sent.')
    #        self.cleaned_data['user'] = user
    #
    #    return super(SigninLocalAccount, self).clean()        