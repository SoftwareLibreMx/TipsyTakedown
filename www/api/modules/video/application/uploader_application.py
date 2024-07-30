from threading import Thread
from werkzeug.datastructures import FileStorage

from shared.globals import db_engine, minion_credentials
from api.libs.domain_entity import FlaskFile

from ..domain.service import VideoUploaderService
from ..infraestructure.repository import VideoEQRepository, MinioRepository

FILE_KEY_PREFIX = 'test_upload_video'

VU_SERVICE = None
VIDEO_EQ_REPOSITORY = None
MINIO_REPOSITORY = None


def __init_classes() -> VideoUploaderService:
    vu_service = globals().get('VU_SERVICE')
    video_eq_repository = globals().get('VIDEO_EQ_REPOSITORY')
    minio_repository = globals().get('MINIO_REPOSITORY')

    if video_eq_repository is None:
        video_eq_repository = VideoEQRepository(db_engine)

    if minio_repository is None:
        minio_repository = MinioRepository(
            minion_credentials.get('endpoint'),
            minion_credentials.get('access_key'),
            minion_credentials.get('secret_key'),
            minion_credentials.get('bucket_name'),
            minion_credentials.get('secure')
        )

    if vu_service is None:
        vu_service = VideoUploaderService(
            FILE_KEY_PREFIX,
            video_eq_repository,
            minio_repository
        )

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

    print('here')
    Thread(target=lambda: vu_service.add_video_file_to_encoding_queue(
        video_id, flask_file)).start()
