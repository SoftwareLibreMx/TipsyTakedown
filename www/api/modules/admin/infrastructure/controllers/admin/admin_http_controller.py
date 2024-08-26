from flask import Blueprint

from ..course.course_http_controller import admin_course_api
from ..material.material_http_controller import admin_material_api

admin_api = Blueprint('admin_api', __name__)

admin_api.register_blueprint(admin_course_api, url_prefix='/course')
admin_api.register_blueprint(admin_material_api, url_prefix='/material')
