from flask import Blueprint, render_template

from shared.utils import abort
from shared.domain.entity import UserType

from ...libs.utils import get_translations, authorizer
from api.modules.admin import application

TEMPLATE_DIR = 'admin'
admin_router = Blueprint('admin', __name__)


@admin_router.route('/')
@authorizer([UserType.ADMIN, UserType.TEACHER])
def index(user):
    return render_template(f'{TEMPLATE_DIR}/index.html',
                           translations=get_translations())


@admin_router.route('/course/new')
@authorizer([UserType.ADMIN, UserType.TEACHER])
def course(user):
    return render_template(f'{TEMPLATE_DIR}/course/create.html',
                           translations=get_translations())


@admin_router.route('/course/<course_id>/edit')
@authorizer([UserType.ADMIN, UserType.TEACHER])
def course_edit(user, course_id):
    errors, course_detail = application.course.get_detail(user, course_id)

    if errors or not course_detail:
        abort(404)

    return render_template(f'{TEMPLATE_DIR}/course/create.html',
                           course=course_detail,
                           translations=get_translations())


@admin_router.route('/video/uploader')
@authorizer([UserType.ADMIN, UserType.TEACHER])
def upload_video():
    return render_template(
        f'{TEMPLATE_DIR}/video/uploader/index.html',
        translations=get_translations())
