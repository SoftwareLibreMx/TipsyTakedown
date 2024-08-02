import shared.jwt as jwt
import datetime
from shared.globals import (
    JWT_SECRET_KEY, JWT_SECRET_ISSUER
)

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'iss': JWT_SECRET_ISSUER,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        if payload['iss'] != JWT_SECRET_ISSUER:
            return 'Invalid token', None
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return 'Token has expired', None
    except jwt.InvalidTokenError:
        return 'Invalid token', None