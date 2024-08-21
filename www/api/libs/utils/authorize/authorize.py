from flask import request
from functools import wraps

from api.libs.utils import abort
from api.libs.domain_entity import UserType
from shared.tipsy_jwt import verify_token


def authorize(user_type_required: UserType = None):
    def login_required(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization', None)
            errors, payload = verify_token(token)

            if errors:
                abort(401, errors)

            return f(payload.get('user', {}), *args, **kwargs)

        return decorated_function

    return login_required
