from flask import (
    Blueprint, render_template, redirect,
    request, url_for, session
)

from shared.utils import abort
from api.modules.course import application

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

    courses.extend(courses)
    courses.extend(courses)

    if errors:
        abort(500)

    return render_template('index.html',
                           translations=get_translations(),
                           courses=courses)


@webapp.route('/change_language/<language>')
def change_language(language):
    session['lang'] = language
    return redirect(request.referrer or url_for('index'))
