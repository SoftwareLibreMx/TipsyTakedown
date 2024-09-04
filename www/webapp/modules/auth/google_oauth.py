from flask import (
    Blueprint, session, redirect, request, render_template
)
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from api.modules.auth.application import google as auth_application
from ...libs.utils.language import get_translations
from shared.globals import google_oauth_credentials
from shared.utils import abort

TEMPLATE_DIR = "auth/google"
google_oauth_router = Blueprint("google", __name__)


@google_oauth_router.route("/")
def login():
    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        google_oauth_credentials.get("cs_file"),
        scopes=google_oauth_credentials.get("scopes", []),
        redirect_uri=google_oauth_credentials.get("redirect_uri", lambda: "")()
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        prompt="select_account",
        include_granted_scopes='true'
    )

    # Save the state so we can verify the request later
    session["state"] = state

    return redirect(authorization_url)


def get_user_info(credentials):
    service = build("people", "v1", credentials=credentials)
    profile = service.people().get(
        resourceName="people/me",
        personFields="names,photos,emailAddresses"
    ).execute()

    user = {}

    for field in profile.get("names", []):
        if field.get("metadata", {}).get("primary", False):
            user["given_name"] = field.get("givenName")
            user["surname"] = field.get("familyName")
            user["openid"] = field.get(
                "metadata", {}).get("source", {}).get("id")

    for field in profile.get("photos", []):
        if field.get("metadata", {}).get("primary", False):
            user["avatar"] = field.get("url")

    for field in profile.get("emailAddresses", []):
        if field.get("metadata", {}).get("primary", False):
            user["email"] = field.get("value")

    return user


@google_oauth_router.route("/callback")
def callback():
    if request.args.get("state") != session["state"]:
        raise Exception("Invalid state")

    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        google_oauth_credentials.get("cs_file"),
        scopes=google_oauth_credentials.get("scopes", []),
        redirect_uri=google_oauth_credentials.get(
            "redirect_uri", lambda: "")(),
        state=session["state"]
    )

    # Exchange the authorization code for an access token
    flow.fetch_token(authorization_response=request.url)

    # Save the credentials to the session
    user_info = get_user_info(flow.credentials)

    error, userc = auth_application.get_or_create_user_token(user_info)

    if error:
        abort(500)

    session["token"] = userc.get("token")

    return render_template(
        f"{TEMPLATE_DIR}/callback.html",
        translations=get_translations('auth'),
        token=userc.get("token")
    )
