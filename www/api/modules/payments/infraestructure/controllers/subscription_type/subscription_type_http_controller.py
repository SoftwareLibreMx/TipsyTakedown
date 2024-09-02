import json
from flask import Blueprint

from api.libs.domain_entity import UserType

from api.libs.utils import api_response as Response, as_json_dumps, dataclass_to_json_dumps
from api.libs.utils import api_authorizer
from api.libs.utils import as_dict

from ....application import subscription_type as subscription_type_app

subscription_type_api = Blueprint('subscription_type_api', __name__)


@subscription_type_api.route('/<subscription_type_id>', methods=['GET'])
# @api_authorizer([UserType.ADMIN, UserType.TEACHER, UserType.STUDENT])
def get(subscription_type_id):
    errors, subscription_type = subscription_type_app.get(subscription_type_id)
    if errors:
        return Response(json.dumps({"errors": errors}), status=404)

    return Response(dataclass_to_json_dumps(subscription_type), status=200)


@subscription_type_api.route('', methods=['GET'])
def all():
    subscription_types = subscription_type_app.get_all()

    return Response(json.dumps(subscription_types), status=200)
