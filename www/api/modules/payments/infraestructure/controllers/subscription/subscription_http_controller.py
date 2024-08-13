from flask import Blueprint, request

from api.libs.utils import api_response as Response, as_json_dumps, authorize

# from .... import application

subscription_api = Blueprint('subscription_api', __name__)


@subscription_api.route('', methods=['POST'])
@authorize()
def subscribe(user):
    request_data = request.get_json()
    print(user)
    print(request_data)

    return Response("{}", status=200)

    # errors, subscription = application.pay_subscription(request_data)

    # if errors:
    #     return Response(as_json_dumps({"errors": errors}), status=400)

    # return Response(as_json_dumps(subscription), status=201)
