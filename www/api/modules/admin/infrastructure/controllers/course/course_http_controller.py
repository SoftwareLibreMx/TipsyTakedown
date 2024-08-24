import json
from flask import Blueprint, request

from api.libs.domain_entity import UserType
from api.libs.utils import (
    api_response as Response, as_json_dumps
)
# from shared.utils.authorizer import authorizer

from .... import application

admin_course_api = Blueprint('admin_course_api', __name__)


@admin_course_api.route('', methods=['POST'])
# @authorizer([UserType.ADMIN, UserType.TEACHER])
def create_course(user):
    errors, course = application.course.create(user, request.get_json())

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(as_json_dumps(course), status=201)
