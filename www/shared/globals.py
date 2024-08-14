import os

from flask import url_for

from dotenv import load_dotenv

from .db_connection import get_db_engine

load_dotenv()

db_engine = get_db_engine(
    user=os.getenv("POSTGRES_USER", "db_user"),
    password=os.getenv("POSTGRES_PASSWORD", "1Passw0rd2345"),
    host=os.getenv("POSTGRES_HOST", "tipsy_db"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    db_name=os.getenv("POSTGRES_DB_NAME", "tipsy_db"),
)

minion_credentials = {
    "access_key": os.getenv("MINIO_ACCESS_KEY", ""),
    "secret_key": os.getenv("MINIO_SECRET_KEY", ""),
    "endpoint": os.getenv("MINIO_ENDPOINT", ""),
    "bucket_name": os.getenv("MINIO_BUCKET_NAME", ""),
    "secure": os.getenv("MINIO_SECURE", False),
}

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = os.getenv(
    "OAUTHLIB_INSECURE_TRANSPORT", "1")
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = os.getenv(
    "OAUTHLIB_RELAX_TOKEN_SCOPE", "1")

google_oauth_credentials = {
    "cs_file": os.getenv(
        "GOOGLE_CLIEN_SECRET_NAME", "client_secret.json"),
    "redirect_uri": (
        lambda: url_for("web.oauth.google.callback", _external=True)),
    "scopes": os.getenv(
        "GOOGLE_SCOPES",
        "https://www.googleapis.com/auth/userinfo.profile,https://www.googleapis.com/auth/userinfo.email"
    ).split(",")
}

mercadopago_credentials = {
    "hidde_user_email_salt": os.getenv(
        "MP_HIDDE_USER_EMAIL_KEY", "$2b$12$vOW3UMIQJqUVr1QVCYQiR."
    ).encode("utf-8"),
    "fake_domain": os.getenv("MP_FAKE_DOMAIN", "foo.com"),
    "access_token": os.getenv("MP_ACCESS_TOKEN", ""),
}

local_prefix = os.getenv("LOCAL_PREFIX", "./tmp")
SECRET_KEY = os.getenv('SECRET_KEY', 'Super Scret Key For Flask App')
jwt_credentials = {
    "jwt_secret_key": os.getenv("JWT_SECRET_KEY", "Super Scret Key For JWT"),
    "jwt_secret_issuer": os.getenv("JWT_SECRET_ISSUER", "Tipsy TakeDown")
}
