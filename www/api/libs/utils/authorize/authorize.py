from typing import Union
from functools import wraps

from flask import request

from api.libs.utils import abort
from api.libs.domain_entity import UserType
from shared.tipsy_jwt import verify_token


def authorize(
    user_type_required: Union[UserType, list[UserType]] = []
):
    if user_type_required and not isinstance(user_type_required, list):
        user_type_required = [user_type_required]

    user_type_required = list(map(lambda x: x.value, user_type_required))

    def login_required(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization', None)
            errors, payload = verify_token(token)

            if errors:
                abort(401, errors)

            from api.modules.auth import application

            if len(user_type_required) > 0:
                errors, user = application.auth.check_user_type(
                    payload.get('user', {}),
                    user_type_required
                )

                if errors:
                    abort(403, 'Forbidden')

            return f(payload.get('user', {}), *args, **kwargs)

        return decorated_function

    return login_required
