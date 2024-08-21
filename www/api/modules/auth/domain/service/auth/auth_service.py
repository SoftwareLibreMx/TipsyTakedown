import jwt
import datetime
from shared.globals import jwt_credentials

from ...dto import UserCDTO
from ..user import UserService
from ..user_credential import UserCredentialService


class AuthService:
    def __init__(self,
                 user_service: UserService,
                 user_credential_service: UserCredentialService):
        self.user_service = user_service
        self.user_credential_service = user_credential_service

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

    def sign_up(self, user_c_dict) -> tuple[list[str], UserCDTO]:
        userc = self.user_service.get_by_email(user_c_dict['email'])

        if userc:
            return ['Email already exists'], None

        errors, user = self.user_service.create(user_c_dict)

        if errors:
            return errors, None

        errors, user_credential = self.user_credential_service.create(
            user.id, user_c_dict)

        if errors:
            return errors, None

        return None, UserCDTO.from_uc(user, user_credential)

    def sign_in(self, email, password) -> tuple[list[str], UserCDTO]:
        userc = self.user_service.get_by_email(email)

        if not userc:
            return ['Not found'], None

        errors, credentials = self.user_credential_service.validate_password(
            email, password)

        if errors:
            return errors, None

        return None, {
            'user': userc,
            'token': self.generate_token(userc)
        }
