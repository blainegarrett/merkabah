from handshake.library.view_tools import render_to_response

#from acsite.handshake.login.models import User
def index(request):
    template_path = 'handshake/jive.html'
    context = {'something': 'welcome'}
    
    return render_to_response(request, template_path, context)
    
    #from handshake.login.models import User, Login
    #u = User(username='blainegarrett', email = 'blaine@blainegarrett.com', confirmed=0, confirmation_key='5r3jek', squelch=0)
    #
    #l = Login(service_type=1, service_key=1, name='jive slice')    
    #u.save()
    #l.user = u
    #l.save()
    #
    #
    #
    #
    
def signin_complete(request):
    from acsite.people import oauthtwitter, oauth
    import acsite.settings as settings    

    request_token = request.session['oauth_request_token']
    oauth_consumer = oauthtwitter.OAuthApi('Vx43QEmSCP1whLq1OSPg', 'GLO2wX1qJrtnO5yBmz8pO8msNoPOBEmUotelZZUfU', request_token)
    access_token = oauth_consumer.getAccessToken()
    access_token_str = oauth.OAuthToken.to_string(access_token)        
    request.session['oauth_access_token_str'] = access_token_str

    # Create a new instance of the Twitter Api and fetch the user's screen name
    oauth_consumer = oauthtwitter.OAuthApi(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, access_token)
    twitter_user = oauth_consumer.GetUserInfo()
    twitter_screen_name = twitter_user.screen_name
    raise Exception(twitter_screen_name)
    
    # Google Version
    access_token = request.GET['token']
    raise Exception(access_token) #<QueryDict: {u'oauth_token': [u'6PI56JKzvdIPO5XFDMbL4EnHte91LGM7NQDgAfqGLE']}>
    
    return render_to_response(request, template_path, context)

def signin(request):
    from acsite.people import oauthtwitter
    import acsite.settings as settings
    
    # Step 1: Create an anonymous twitter oauth consumer
    oauth_consumer = oauthtwitter.OAuthApi('Vx43QEmSCP1whLq1OSPg', 'GLO2wX1qJrtnO5yBmz8pO8msNoPOBEmUotelZZUfU') # Blaine's Personal Dev Site keys
    #oauth_consumer = oauthtwitter.OAuthApi(u'HIOPxqeLyXCbCtkZsaT3g', u'lyzNa3MhzkaFUs8KuOmmYf0Ejq2kI77QTq4r3SSDA3g') # Propeller.com Dev Site keys
    #oauth_consumer = oauthtwitter.OAuthApi(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    # Step 2: Fetch Request Token From Twitter
    request_token = oauth_consumer.getRequestToken()
    
    # Redirect them to the url
    authorization_url = oauth_consumer.getAuthorizationURL(request_token) 

    request.session['oauth_type'] = 'twitter'
    request.session['oauth_request_token'] = request_token
    raise Exception(authorization_url)

    template_path = 'handshake/jive.html'
    context = {'something': 'welcome'}
    
    return render_to_response(request, template_path, context)

def twitter(request):
    from acsite.people import twitter
    api = twitter.Api(username='blainegarrett', password='5an2sAran')
    users = api.GetUser('blainegarrett')
    raise Exception([u.name for u in users])