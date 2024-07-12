from flask import Blueprint

from ... import application

video_api = Blueprint('video_api', __name__)


@video_api.route('/<int:video_id>', methods=['GET'])
def get_video_url(video_id):
    return application.get_video_by_id(video_id)
