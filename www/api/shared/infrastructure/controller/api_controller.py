from flask import Blueprint

from api.modules.video.infraestructure.controller import video_api

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return 'OK'


api.register_blueprint(video_api, url_prefix='/video')
