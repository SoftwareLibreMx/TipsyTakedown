import json
from flask import Blueprint, request

from api.libs.domain_entity import UserType
from api.libs.utils import (
    api_response as Response, as_json_dumps
)
from api.libs.utils import api_authorizer

from .... import application

admin_course_api = Blueprint('admin_course_api', __name__)


@admin_course_api.route('', methods=['POST'])
@api_authorizer([UserType.ADMIN, UserType.TEACHER])
def create_course(user):
    request_data = (
        request.form.to_dict()
        if request.content_type != 'application/json' else
        request.get_json()
    )

    thumbnail_file = request.files.get('thumbnail', None)
    if not request_data.get('thumbnail', None) and not thumbnail_file:
        return Response(
            json.dumps({"errors": ["Thumbnail is required"]}),
            status=400
        )

    errors, course = application.course.create(user, request_data)

    application.course.add_thumbnail_to_course_async(
        course.id, thumbnail_file
    )

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(as_json_dumps(course), status=201)


@admin_course_api.route('/<course_id>', methods=['get'])
@api_authorizer([UserType.ADMIN, UserType.TEACHER])
def get_course_detail(user, course_id):
    errors, course = application.course.get_detail(user, course_id)

    if errors:
        return Response(json.dumps({"errors": errors}), status=400)

    return Response(json.dumps(course, default=str), status=200)
