from flask import Blueprint, render_template

TEMPLATE_DIR = 'admin'
admin_router = Blueprint('admin', __name__)


@admin_router.route('/')
def index():
    return render_template(f'{TEMPLATE_DIR}/index.html')


@admin_router.route('/video/uploader')
def upload_video():
    return render_template(f'{TEMPLATE_DIR}/video/uploader/index.html')
