from flask import Blueprint, render_template

from ...libs.utils.language import get_translations

TEMPLATE_DIR = 'admin'
admin_router = Blueprint('admin', __name__)


@admin_router.route('/')
def index():
    return render_template(f'{TEMPLATE_DIR}/index.html',
                           translations=get_translations())


@admin_router.route('/course/new')
def course():
    return render_template(f'{TEMPLATE_DIR}/course/create.html',
                           translations=get_translations())


@admin_router.route('/video/uploader')
def upload_video():
    return render_template(
        f'{TEMPLATE_DIR}/video/uploader/index.html', translations=get_translations())
