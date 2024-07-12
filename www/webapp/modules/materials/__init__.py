from flask import Blueprint
from .video import video_router

materials_router = Blueprint('materials', __name__)

materials_router.register_blueprint(video_router, url_prefix='/video')
