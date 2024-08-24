from threading import Thread

from werkzeug.datastructures import FileStorage

from shared.globals import db_engine, minion_credentials

from api.libs.domain_entity import FlaskFile
from api.modules.video.domain.service import (
    FFMPEGService, VideoEncoderService, VideoUploaderService
)
from api.modules.video.infraestructure.repository import (
    VideoEQRepository, MinioRepository, FFMPEGRepository
)

FILE_KEY_PREFIX = 'not_encoded'

VIDEO_EQ_REPOSITORY = None
FFMPEG_REPOSITORY = None
FFMPEG_SERVICE = None
MINIO_REPOSITORY = None
VIDEO_ENCODER_SERVICE = None
VU_SERVICE = None


def __init_classes():
    global VIDEO_EQ_REPOSITORY, FFMPEG_REPOSITORY, FFMPEG_SERVICE
    global MINIO_REPOSITORY, VIDEO_ENCODER_SERVICE, VU_SERVICE

    if VIDEO_EQ_REPOSITORY is None:
        VIDEO_EQ_REPOSITORY = VideoEQRepository(db_engine)

    if FFMPEG_REPOSITORY is None:
        FFMPEG_REPOSITORY = FFMPEGRepository()

    if FFMPEG_SERVICE is None:
        FFMPEG_SERVICE = FFMPEGService(FFMPEG_REPOSITORY)

    if MINIO_REPOSITORY is None:
        MINIO_REPOSITORY = MinioRepository(
            minion_credentials.get('endpoint'),
            minion_credentials.get('access_key'),
            minion_credentials.get('secret_key'),
            minion_credentials.get('bucket_name'),
            minion_credentials.get('secure')
        )

    if VIDEO_ENCODER_SERVICE is None:
        VIDEO_ENCODER_SERVICE = VideoEncoderService(
            VIDEO_EQ_REPOSITORY,
            FFMPEG_SERVICE,
            MINIO_REPOSITORY
        )

    if VU_SERVICE is None:
        VU_SERVICE = VideoUploaderService(
            FILE_KEY_PREFIX,
            VIDEO_EQ_REPOSITORY,
            MINIO_REPOSITORY
        )

    return VIDEO_ENCODER_SERVICE, VU_SERVICE


def process_video_queue():
    video_encoder_service, _ = __init_classes()

    video_encoder_service.encode_fifo()


def encode_video(video_queue_id: str):
    video_encoder_service, _ = __init_classes()

    video_encoder_service.encode(video_queue_id)


def add_video_file_to_encoding_queue_async(
        video_id: str, video_file: FileStorage):
    if not video_file:
        return

    _, vu_service = __init_classes()

    video_file_bytes = video_file.read()

    flask_file = FlaskFile(
        file_name=video_file.filename,
        mimetype=video_file.mimetype,
        file_size=len(video_file_bytes),
        content=video_file_bytes
    )

    Thread(target=lambda: vu_service.add_video_file_to_encoding_queue(
        video_id, flask_file)).start()
