import json
from flask import Blueprint

from api.libs.utils import api_response as Response

from ....application.subscription_type import get_all

subscription_type_api = Blueprint('subscription_type_api', __name__)


@subscription_type_api.route('', methods=['GET'])
def all():
    subscription_types = get_all()

    return Response(json.dumps(subscription_types), status=200)
