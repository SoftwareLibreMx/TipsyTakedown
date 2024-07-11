from flask import Blueprint, render_template

video_router = Blueprint('video', __name__)


def get_video_url(video_id):
    # This is a placeholder function that would return the video URL
    return 'https://www.youtube.com/watch?v=abc123'


@video_router.route('/<int:video_id>')
def show(video_id):
    video_source = get_video_url(video_id)

    return render_template('material/videoPlayer.html', video_source=video_source)
