import jwt
from typing import Union, Optional
from functools import wraps

from flask import session

from shared.utils import abort

from shared.domain.entity import UserType
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


def authorizer(
    user_type_required: Union[UserType, list[UserType]] = []
):
    if user_type_required and not isinstance(user_type_required, list):
        user_type_required = [user_type_required]

    user_type_required = list(map(lambda x: x.value, user_type_required))

    def login_required(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = session.get('token', None)
            errors, payload = verify_token(token)

            if errors:
                abort(401)

            from api.modules.auth import application

            if len(user_type_required) > 0:
                errors, user = application.auth.check_user_type(
                    payload.get('user', {}),
                    user_type_required
                )

                if errors:
                    abort(403)

            return f(payload.get('user', {}), *args, **kwargs)

        return decorated_function

    return login_required
