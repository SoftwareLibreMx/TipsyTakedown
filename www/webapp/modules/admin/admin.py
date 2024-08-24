from flask import Blueprint, render_template

# from shared.utils.authorizer import authorizer

TEMPLATE_DIR = 'admin'
admin_router = Blueprint('admin', __name__)


@admin_router.route('/')
# @authorizer([])
def index():
    return render_template(f'{TEMPLATE_DIR}/index.html', courses=[])


@admin_router.route('/video/uploader')
# @authorizer([])
def upload_video():
    return render_template(f'{TEMPLATE_DIR}/video/uploader/index.html')
