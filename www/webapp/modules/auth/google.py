from flask import Blueprint, redirect, url_for, session, render_template, request
from flask_oauthlib.client import OAuth

google = Blueprint('google', __name__)
oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key='CLIENT_KEY',
    consumer_secret='SECRET_APP',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@google.route('/login')
def login():
    return google.authorize(callback=url_for('google.authorized', _external=True))

@google.route('/logout')
def logout():
    session.pop('google_token')
    return redirect(url_for('web.index'))

@google.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    return render_template('auth.google.callback.html', user_info=user_info.data)

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')