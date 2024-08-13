import jwt
import datetime
from shared.globals import jwt_credentials
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'iss': jwt_credentials.get('jwt_issuer'),
        'exp': datetime.datetime.now() + datetime.timedelta(days=7)
    }
    token = jwt.encode(payload, jwt_credentials.get('jwt_secret_key'), algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, jwt_credentials.get('jwt_secret_key'), algorithms=['HS256'])
        if payload['iss'] != jwt_credentials.get('jwt_issuer'):
            return 'Invalid token', None
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return 'Token has expired', None
    except jwt.InvalidTokenError:
        return 'Invalid token', None