import asyncio
import json
from flask import Blueprint, request

from api.shared.infraestructure.utils import api_response as Response, as_json_dumps

from ... import application

video_api = Blueprint('video_api', __name__)


@video_api.route('/<video_id>', methods=['GET'])
def get_video_url(video_id):
    video = application.get_video_by_id(video_id)

    if not video:
        return Response(json.dumps(
            {"errors": ["Video not found"]}), status=404)

    return Response(as_json_dumps(video), status=200)


@video_api.route('/', methods=['POST'])
async def create_video():
    request_data = request.get_json(
    ) if request.headers['Content-Type'] == 'application/json' else request.form

    errors, video = application.create_video(request_data)

    if errors:
        print(errors)
        return Response(json.dumps({"errors": errors}), status=400)

    # Exec async function to save video file
    request.files.get('video_file', None)

    return Response(as_json_dumps(video), status=201)


@video_api.route('/<video_id>', methods=['PATCH'])
def update_video(video_id):
    request_data = request.get_json()

    errors, video = application.update_video(video_id, request_data)

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(as_json_dumps(video), status=200)


@video_api.route('/<video_id>', methods=['DELETE'])
def delete_video(video_id):
    errors = application.delete_video(video_id)

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(status=204)
