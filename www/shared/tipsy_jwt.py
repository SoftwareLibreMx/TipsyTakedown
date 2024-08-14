import jwt
from typing import Optional

from shared.globals import jwt_credentials


def verify_token(token) -> tuple[Optional[str], Optional[str]]:
    secret_key = jwt_credentials.get('jwt_secret_key', '')

    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return 'Token has expired', None
    except jwt.InvalidTokenError:
        return 'Invalid token', None

    if payload.get('iss', '') != jwt_credentials.get('jwt_issuer'):
        return 'Invalid token', None

    return None, payload
