from flask import Blueprint, request

from api.libs.utils import (
    api_response as Response,
    as_json_dumps,
    # authorize
)

from .... import application

subscription_api = Blueprint('subscription_api', __name__)


@subscription_api.route('', methods=['POST'])
# @authorize()
def subscribe():
    request_data = request.get_json()

    # TODO: REMOVE THIS
    user = request_data.get('user')

    errors, subscription = application.pay_subscription(
        user,
        request_data.get('subscription_type_id'),
        request_data.get('payment_method'),
        request_data.get('promo_code'),
        request_data.get('card'),
    )

    if errors:
        return Response(as_json_dumps({"errors": errors}), status=400)

    return Response(as_json_dumps(subscription), status=201)
