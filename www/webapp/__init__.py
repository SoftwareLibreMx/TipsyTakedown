from flask import Blueprint, render_template, redirect, url_for, session
# from authlib.integrations.flask_client import OAuth
# from app import oauth

from .modules.materials import materials_router

webapp = Blueprint('web', __name__)

webapp.register_blueprint(materials_router, url_prefix='/material')


# # Configure the Google OAuth client
# google = oauth.register(
#     name='google',
#     client_id='YOUR_CLIENT_ID',
#     client_secret='YOUR_CLIENT_SECRET',
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     # authorize_params=None,
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     # access_token_params=None,
#     # refresh_token_url=None,
#     redirect_uri='http://localhost:8000/auth/google',
#     client_kwargs={'scope': 'openid profile email'}
# )
# # Configure the Facebook OAuth client
# facebook = oauth.register(
#     name='facebook',
#     client_id='YOUR_CLIENT_ID',
#     client_secret='YOUR_CLIENT_SECRET',
#     authorize_url='https://www.facebook.com/dialog/oauth',
#     # authorize_params=None,
#     access_token_url='https://graph.facebook.com/oauth/access_token',
#     # access_token_params=None,
#     # refresh_token_url=None,
#     redirect_uri='http://localhost:8000/auth/facebook',
#     client_kwargs={'scope': 'email'}
# )

@webapp.route('/')
def index():
    return render_template("index.html")

@webapp.route('/login')
def login():
    return render_template("login.html")

# # GOOGLE LOGIN ROUTES 
# @webapp.route('/login/google')
# def login_google():
#     redirect_uri = url_for('auth.authorize', _external=True)
#     return google.authorize_redirect(redirect_uri)

# @webapp.route('/auth/google')
# def auth_google():
#     token = google.authorize_access_token()
#     user_info = google.parse_id_token(token)
#     session['user'] = user_info
#     return redirect('/')

# # FACEBOOK LOGIN ROUTES
# @webapp.route('/login/facebook')
# def login_facebook():
#     redirect_uri = url_for('auth.facebook_authorize', _external=True)
#     return facebook.authorize_redirect(redirect_uri)

# @webapp.route('/auth/facebook')
# def auth_facebook():
#     token = facebook.authorize_access_token()
#     user_info = facebook.get('https://graph.facebook.com/me?fields=id,name,email', token=token).json()
#     session['user'] = user_info
#     return redirect('/')
