from flask import Blueprint

from api.libs.domain_entity import UserType
from api.libs.utils import authorize

admin_course_api = Blueprint('admin_course_api', __name__)


@admin_course_api.route('', methods=['POST'])
@authorize([UserType.ADMIN, UserType.TEACHER])
def create_course(user):
    return 'create_course'
