import json
from flask import Blueprint, request

from api.libs.domain_entity import UserType
from api.libs.utils import api_response as Response
from api.libs.utils import api_authorizer

from .... import application

admin_lesson_api = Blueprint('admin_lesson_api', __name__)


@admin_lesson_api.route('', methods=['GET'])
@api_authorizer([UserType.ADMIN, UserType.TEACHER])
def search_by_name(user):
    query = request.args.get('query')

    lessons = application.lesson.search_by_name(query)

    return Response(json.dumps(lessons, default=str), status=200)


@admin_lesson_api.route('/<lesson_id>', methods=['GET'])
@api_authorizer([UserType.ADMIN, UserType.TEACHER])
def get_lesson_detail_admin(user, lesson_id):
    error, lessons = application.lesson.get_detail_by_id(lesson_id)

    if error:
        return Response(json.dumps({"errors": error}), status=404)

    return Response(json.dumps(lessons, default=str), status=200)
