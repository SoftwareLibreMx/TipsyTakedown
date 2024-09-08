import json
from flask import (
    Blueprint, render_template, Response, redirect
)

# from api.modules.video.application import get_video_by_id
from api.modules.admin.application.material import material_application as material

from ...libs.utils import get_translations
TEMPLATE_DIR = 'video'
video_router = Blueprint('video', __name__)


@video_router.route('/<video_id>')
def show(video_id):
    errors, video = material.get_by_id(video_id)

    if errors:
        return redirect('/error/404')

    return render_template(f'{TEMPLATE_DIR}/index.html',
                           video=video,
                           translations=get_translations(),
                           video_src=video.urls[0])
