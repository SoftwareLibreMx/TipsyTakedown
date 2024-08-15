import jwt
import datetime

from shared.globals import jwt_credentials

from ...dto import UserCDTO


class AuthService:
    def generate_token(self, user: UserCDTO) -> str:
        payload = {
            'user': {
                'id': str(user.id),
                'user_type': str(user.user_type),
                'email': user.email,
                'given_name': user.given_name,
                'surname': user.surname,
                'avatar': user.avatar
            },
            'iss': jwt_credentials.get('jwt_issuer'),
            'exp': datetime.datetime.now() + datetime.timedelta(days=7)
        }

        jwt_secret_key = jwt_credentials.get('jwt_secret_key')

        return jwt.encode(payload, jwt_secret_key, algorithm='HS256')
