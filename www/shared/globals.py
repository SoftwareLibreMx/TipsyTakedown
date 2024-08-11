import os

from dotenv import load_dotenv

from .db_connection import get_db_engine

load_dotenv()

db_engine = get_db_engine(
    user=os.getenv('POSTGRES_USER', 'db_user'),
    password=os.getenv('POSTGRES_PASSWORD', '1Passw0rd2345'),
    host=os.getenv('POSTGRES_HOST', 'tipsy_db'),
    port=os.getenv('POSTGRES_PORT', '5432'),
    db_name=os.getenv('POSTGRES_DB_NAME', 'tipsy_db'))

minion_credentials = {
    'access_key': os.getenv('MINIO_ACCESS_KEY', ''),
    'secret_key': os.getenv('MINIO_SECRET_KEY', ''),
    'endpoint': os.getenv('MINIO_ENDPOINT', ''),
    'bucket_name': os.getenv('MINIO_BUCKET_NAME', ''),
    'secure': os.getenv('MINIO_SECURE', False)
}

google_oauth_credentials = {
    'client_id': os.getenv('GOOGLE_OAUTH_CLIENT_ID', ''),
    'client_secret': os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', ''),
    'redirect_uri': os.getenv('GOOGLE_OAUTH_REDIRECT_URI', '')
}
mercadopago_credentials = {
    'hidde_user_email_salt': os.getenv(
        'MP_HIDDE_USER_EMAIL_KEY',
        '$2b$12$vOW3UMIQJqUVr1QVCYQiR.'
    ).encode('utf-8'),
    'fake_domain': os.getenv('MP_FAKE_DOMAIN', 'foo.com'),
    'access_token': os.getenv('MP_ACCESS_TOKEN', ''),
}

local_prefix = os.getenv('LOCAL_PREFIX', './tmp')

SECRET_KEY = os.getenv('SECRET_KEY', 'Super Scret Key For Flask App')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'Super Scret Key For JWT')
JWT_SECRET_ISSUER = os.getenv('JWT_SECRET_ISSUER', 'Tipsy TakeDown')
