from flask import Blueprint

from .create_course import create_course_router

course_router = Blueprint('courses', __name__)

course_router.register_blueprint(create_course_router, url_prefix='/create')
