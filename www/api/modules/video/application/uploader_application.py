from threading import Thread
from werkzeug.datastructures import FileStorage

from shared.globals import db_engine
from api.libs.domain_entity import FlaskFile

from ..domain.service import VideoUploaderService
from ..infraestructure.repository import VideoEQRepository

vu_service = None
video_eq_repository = None


def __init_classes() -> VideoUploaderService:
    vu_service = globals().get('vu_service')
    video_eq_repository = globals().get('video_eq_repository')

    if video_eq_repository is None:
        video_eq_repository = VideoEQRepository(db_engine)

    if vu_service is None:
        vu_service = VideoUploaderService(
            'test_upload_video', video_eq_repository)

    return vu_service


def add_video_file_to_encoding_queue_async(
        video_id: str, video_file: FileStorage):
    if not video_file:
        return

    vu_service = __init_classes()

    video_file_bytes = video_file.read()

    flask_file = FlaskFile(
        file_name=video_file.filename,
        mimetype=video_file.mimetype,
        file_size=len(video_file_bytes),
        content=video_file_bytes
    )

    Thread(target=lambda: vu_service.add_video_file_to_encoding_queue(
        video_id, flask_file)).start()
