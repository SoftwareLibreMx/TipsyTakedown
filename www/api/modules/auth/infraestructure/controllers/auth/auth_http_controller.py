import json
from dataclasses import asdict

from flask import Blueprint, request

from api.libs.utils import (
    api_response as Response,
    dataclass_to_json_dumps
)

from ....application import auth as application

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('sign_up', methods=['POST'])
def sign_up():
    request_data = request.get_json()

    errors, userc = application.sign_up(
        request_data
    )

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(dataclass_to_json_dumps(userc), status=201)


@auth_api.route('sign_in', methods=['POST'])
def sign_in():
    request_data = request.get_json()

    errors, userc_token = application.sign_in(
        request_data.get('email'),
        request_data.get('password')
    )

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(json.dumps({
        'token': userc_token.get('token'),
        'user': asdict(userc_token.get('user'))
    }, default=str), status=200)
