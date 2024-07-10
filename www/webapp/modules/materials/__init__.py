from flask import Blueprint
from .video import video

materials = Blueprint('materials', __name__)

materials.register_blueprint(video)
