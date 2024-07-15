import flask
from flask import redirect, url_for, session
from webapp import webapp
from api.shared.infraestructure.controller import api
from authlib.integrations.flask_client import OAuth

def create_app():
    flask_app = flask.Flask(
        __name__,
        template_folder='webapp/templates',
        static_folder='webapp/static')

    # Initialize OAuth
    oauth = OAuth(flask_app)
    # Configure the Google OAuth client
    google = oauth.register(
        name='google',
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        # authorize_params=None,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        # access_token_params=None,
        # refresh_token_url=None,
        redirect_uri='http://localhost:5000/auth',
        client_kwargs={'scope': 'openid profile email'}
    )
    # Configure the Facebook OAuth client
    facebook = oauth.register(
        name='facebook',
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        authorize_url='https://www.facebook.com/dialog/oauth',
        # authorize_params=None,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        # access_token_params=None,
        # refresh_token_url=None,
        redirect_uri='http://localhost:5000/auth/facebook',
        client_kwargs={'scope': 'email'}
    )

    @flask_app.route('/health')
    def health():
        return 'OK'

    # GOOGLE LOGIN ROUTES 
    @flask_app.route('/login/google')
    def login_google():
        redirect_uri = url_for('auth', _external=True)
        return google.authorize_redirect(redirect_uri)

    @flask_app.route('/auth/google')
    def auth_google():
        token = google.authorize_access_token()
        user_info = google.parse_id_token(token)
        session['email'] = user_info['email']
        return redirect('/')

    # FACEBOOK LOGIN ROUTES
    @flask_app.route('/login/facebook')
    def login_facebook():
        redirect_uri = url_for('auth_facebook', _external=True)
        return facebook.authorize_redirect(redirect_uri)

    @flask_app.route('/auth/facebook')
    def auth_facebook():
        token = facebook.authorize_access_token()
        resp = facebook.get('https://graph.facebook.com/me?fields=id,name,email', token=token)
        user_info = resp.json()
        session['email'] = user_info.get('email')
        return redirect('/')

    flask_app.register_blueprint(webapp)
    flask_app.register_blueprint(api, url_prefix='/api/')

    return flask_app


flask_app = create_app()

if __name__ == '__main__':
    flask_app.run()
