import json
from flask import Blueprint, request

from api.libs.utils import (
    api_response as Response,
    as_json_dumps,
    dataclass_to_json_dumps
)

from .... import application

material_api = Blueprint('material_api', __name__)


@material_api.route('/<material_id>', methods=['GET'])
def get_material_by_id(material_id):
    errors, material = application.material.get_by_id(material_id)

    if not errors:
        return Response(json.dumps({"errors": errors}), status=404)

    return Response(as_json_dumps(material), status=200)


@material_api.route('/', methods=['POST'])
def create_material():
    request_data = (request.get_json()
                    if request.headers['Content-Type'] == 'application/json'
                    else request.form)

    errors, material = application.material.create(request_data)

    if errors:
        print(errors)
        return Response(json.dumps({"errors": errors}), status=400)

    material_file = request.files.get('video', None)

    application.video_encoding.add_video_file_to_encoding_queue_async(
        material.id, material_file
    )

    return Response(dataclass_to_json_dumps(material), status=201)


@material_api.route('/<material_id>', methods=['PATCH'])
def update_material(material_id):
    request_data = request.get_json()

    errors, material = application.material.update(material_id, request_data)

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(as_json_dumps(material), status=200)


@material_api.route('/<material_id>', methods=['DELETE'])
def delete_material(material_id):
    errors, _ = application.material.delete(material_id)

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(status=204)
