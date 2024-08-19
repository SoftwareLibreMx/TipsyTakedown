from flask import Blueprint, request

from api.libs.utils import (
    api_response as Response,
    as_json_dumps
)

from ....application import auth as application

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('sign_up', methods=['POST'])
def sign_up():
    request_data = request.get_json()

    errors, user = application.sign_up(
        request_data
    )

    if errors:
        return Response(as_json_dumps({"errors": errors}), status=400)

    return Response(as_json_dumps(user), status=201)