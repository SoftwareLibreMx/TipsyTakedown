from flask import (
    Blueprint, url_for, session, redirect, request
)

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google_auth_oauthlib.flow import InstalledAppFlow

from shared.globals import google_oauth_credentials

google_oauth_router = Blueprint('google', __name__)

AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'

CLIENT_ID = google_oauth_credentials.get('client_id', '')
CLIENT_SECRET = google_oauth_credentials.get('client_secret', '')
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


@google_oauth_router.route('/')
def login():
    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('web.oauth.google.callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='select_account')

    # Save the state so we can verify the request later
    session['state'] = state

    return redirect(authorization_url)


@google_oauth_router.route('/callback')
def callback():
    # Verify the request state
    if request.args.get('state') != session['state']:
        raise Exception('Invalid state')

    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, state=session['state'])
    flow.redirect_uri = url_for('callback', _external=True)

    # Exchange the authorization code for an access token
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Save the credentials to the session
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for(''))
