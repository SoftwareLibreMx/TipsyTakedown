from flask import Blueprint

from api.modules.video.infraestructure.controllers import video_api

api = Blueprint('api', __name__)

api.register_blueprint(video_api, url_prefix='/video')
