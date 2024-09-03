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
