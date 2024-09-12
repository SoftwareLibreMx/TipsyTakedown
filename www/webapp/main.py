from flask import (
    Blueprint, render_template, redirect,
    request, url_for, session
)
from urllib.parse import urljoin

from shared.utils import abort
from api.modules.course import application
# www/api/modules/admin/application/lesson/lesson_application.py
from api.modules.admin.application.lesson.lesson_application import get_by_ids
from .libs.utils.language import get_translations

from .modules.admin import admin_router
from .modules.auth import oauth_router
from .modules.checkout import checkout_router
from .modules.course import course_router
from .modules.errors import error_router
from .modules.video import video_router


webapp = Blueprint('web', __name__)

webapp.register_blueprint(admin_router, url_prefix='/admin')
webapp.register_blueprint(oauth_router, url_prefix='/auth')
webapp.register_blueprint(checkout_router, url_prefix='/checkout')
webapp.register_blueprint(course_router, url_prefix='/course')
webapp.register_blueprint(error_router, url_prefix='/error')
webapp.register_blueprint(video_router, url_prefix='/video')


@webapp.route('/')
def index():
    if request.args.get('token'):
        session['token'] = request.args.get('token')
        return redirect('/')

    errors, courses = application.course.get_all(
        filters={},
        pagination={'page': 1, 'per_page': 10}
    )
    base_url = request.url_root
    courses_materials = []
    for course in courses:
        if course['lessons']:
            lessons = get_by_ids(course['lessons'])
            for lesson in lessons:
                if lesson['materials']:
                    courses_materials.append({
                        'course_id': course.get('id'),
                        'course_name': course.get('name'),
                        'course_thumbnail': urljoin(base_url, course.get('thumbnail')),
                        'material_id': lesson['materials'][0],
                    })

    if errors:
        abort(500)

    return render_template('index.html',
                           translations=get_translations(),
                           courses=courses_materials)


@webapp.route('/change_language/<language>')
def change_language(language):
    session['lang'] = language
    return redirect(request.referrer or url_for('index'))
