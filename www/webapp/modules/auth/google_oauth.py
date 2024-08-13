import json
from flask import Blueprint, url_for, session, redirect, request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from shared.tipsy_jwt import generate_token
from api.modules.auth import application as auth_application
from api.modules.user import application as user_application
import os

# config, set the environment variables for development only
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

google_oauth_router = Blueprint("google", __name__)

CLIENT_SECRET_FILE = "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email"
]


@google_oauth_router.route("/")
def login():
    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for("web.oauth.google.callback", _external=True)
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        prompt="select_account",
        include_granted_scopes='true'
    )
    # Save the state so we can verify the request later
    session["state"] = state

    return redirect(authorization_url)


def credentials_to_dict(credentials):
    # Used by Google OAuth
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
        "id_token": credentials.id_token,
    }


def serialize_credentials(credentials):
    credentials_dict = credentials_to_dict(credentials)
    return json.dumps(credentials_dict)


def get_user_info(credentials):
    service = build("people", "v1", credentials=credentials)
    profile = service.people().get(resourceName="people/me",
                                   personFields="names,photos,emailAddresses").execute()

    names = profile.get("names", [{}])[0]
    given_name = names.get("givenName", "No Given Name")
    family_name = names.get("familyName", "No Family Name")
    avatar = profile.get("photos", [{}])[0].get("url", "No Avatar")
    email = profile.get("emailAddresses", [{}])[0].get("value", "No Email")
    open_id = profile.get("resourceName", "No OpenID")

    return {
        "given_name": given_name,
        "surname": family_name,
        "avatar": avatar,
        "email": email,
        "openid": open_id,
    }


@google_oauth_router.route("/callback")
def callback():
    # Verify the request state
    if request.args.get("state") != session["state"]:
        raise Exception("Invalid state")
    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, state=session["state"]
    )
    flow.redirect_uri = url_for("web.oauth.google.callback", _external=True)

    # Exchange the authorization code for an access token
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Save the credentials to the session
    credentials = flow.credentials
    user_info = get_user_info(credentials)

    user_credential = auth_application.get_user_credential_by_email(
        email=user_info["email"])

    if not user_credential:
        errors, new_user = user_application.create_user(user_info)
        print(errors)
        user_info["user_id"] = str(new_user.id)
        user_info["sso_provider"] = "GOOGLE"
        errors, user_credential = auth_application.create_user_credential_sso(
            user_info)
        print(errors)

    session['user'] = user_info
    session["credentials"] = serialize_credentials(credentials)
    token = generate_token(str(user_credential.id))

    return redirect(url_for("web.client_callback", token=token))
