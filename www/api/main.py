from flask import Blueprint

from api.modules.payments.infraestructure.controllers import payment_api
from api.modules.video.infraestructure.controllers import video_api

api = Blueprint('api', __name__)

api.register_blueprint(payment_api, url_prefix='/payment')
api.register_blueprint(video_api, url_prefix='/video')
