from flask import Blueprint

from ..course.course_http_controller import admin_course_api

admin_api = Blueprint('admin_api', __name__)

admin_api.register_blueprint(admin_course_api, url_prefix='/course')
