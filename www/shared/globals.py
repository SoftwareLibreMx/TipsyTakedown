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
    'client_id': os.getenv('GOOGLE_OAUTH_CLIENT_id', ''),
    'client_secret': os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', ''),
    'redirect_uri': os.getenv('GOOGLE_OAUTH_REDIRECT_URI', '')
}

local_prefix = os.getenv('LOCAL_PREFIX', './tmp')

SECRET_KEY = os.getenv('SECRET_KEY', 'Super Scret Key For Flask App')
