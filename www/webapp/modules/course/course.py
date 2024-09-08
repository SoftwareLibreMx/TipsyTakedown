from flask import Blueprint, render_template

from shared.utils import abort

from ...libs.utils import authorizer, get_translations
from api.modules.admin import application
from api.modules.admin.application.material import (
    material_application as m_application
)

TEMPLETE_DIR = 'course'
course_router = Blueprint('course', __name__)


@course_router.route('/<course_id>/material/<material_id>')
@authorizer()
def course_material(user, course_id, material_id):
    errors, course_detail = application.course.get_detail(user, course_id)

    if errors or not course_detail:
        abort(404)

    for lesson in course_detail.get('lessons', []):
        print(lesson)
        for meterial in lesson.get('materials', []):
            if str(meterial.get('id', None)) == material_id:
                errors, video = m_application.get_by_id(material_id)
                return render_template(f'{TEMPLETE_DIR}/material.html',
                                       material=video,
                                       video_src=video.urls[0],
                                       course=course_detail,
                                       translations=get_translations())

    abort(404)
