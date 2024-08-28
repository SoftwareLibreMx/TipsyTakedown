import json

from flask import Blueprint, request

from api.libs.utils import api_response as Response, as_dict, api_authorizer

from ....application.subscription import pay_subscription

subscription_api = Blueprint('subscription_api', __name__)


@subscription_api.route('', methods=['POST'])
@api_authorizer()
def subscribe(user: dict):
    request_data = request.get_json()

    errors, subscription = pay_subscription(
        user,
        request_data.get('subscription_type_id'),
        request_data.get('payment_method'),
        request_data.get('promo_code'),
        request_data.get('card', {}),
    )

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(json.dumps({
        'subscription': as_dict(subscription.get('subscription')),
        'payment_audit_log': as_dict(subscription.get('payment_audit_log')),
        'payment_response': subscription.get('payment_response', {}),
    }, default=str), status=201)
