import json
from flask import Blueprint, request

from api.shared.infraestructure.utils import api_response as Response, as_json_dumps

from ... import application

video_api = Blueprint('video_api', __name__)


@video_api.route('/<int:video_id>', methods=['GET'])
def get_video_url(video_id):
    return application.get_video_by_id(video_id)


@video_api.route('/', methods=['POST'])
def create_video():
    request_data = request.get_json()

    errors, video = application.create_video(request_data)

    if errors:
        print(errors)
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(as_json_dumps(video), status=201)
