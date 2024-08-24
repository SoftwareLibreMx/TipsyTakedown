from flask import Blueprint

# from api.modules.video.application import get_video_by_id

TEMPLATE_DIR = 'video'
video_router = Blueprint('video', __name__)


@video_router.route('/<video_id>')
def show(video_id):
    # TODO: migrate to course module
    pass
    # errors, video = get_video_by_id(video_id)

    # if errors:
    #     return redirect('/error/404')

    # return render_template(f'{TEMPLATE_DIR}/index.html',
    #                        video=video,
    #                        video_src=video.urls[0])
