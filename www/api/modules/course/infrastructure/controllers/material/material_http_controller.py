import json
from flask import Blueprint, request

from api.libs.utils import (
    api_authorizer, api_response as Response
)

from .... import application

material_api = Blueprint('material_api', __name__)


@material_api.route('', methods=['POST', 'GET'])
@api_authorizer()
def get_materials(user):
    request_data = request.get_json()
    query_params = request.args.to_dict()

    filters = {}
    if 'filters' in request_data:
        filters = request_data['filters']
        del request_data['filters']

    errors, materials_paginated = application.material.get_all(filters, {
        'page': int(query_params.get('page', 1)),
        'per_page': int(query_params.get('per_page', 10)),
    })

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(json.dumps(materials_paginated, default=str), status=200)
