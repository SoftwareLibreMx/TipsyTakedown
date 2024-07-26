from shared.globals import db_engine, minion_credentials

from api.modules.video.domain.service import (
    FFMPEGService, VideoEncoderService
)
from api.modules.video.infraestructure.repository import (
    VideoEQRepository, MinioRepository, FFMPEGRepository
)

VIDEO_EQ_REPOSITORY = None
FFMPEG_REPOSITORY = None
FFMPEG_SERVICE = None
MINIO_REPOSITORY = None
VIDEO_ENCODER_SERVICE = None


def __init_classes():
    global VIDEO_EQ_REPOSITORY, FFMPEG_REPOSITORY, FFMPEG_SERVICE, MINIO_REPOSITORY, VIDEO_ENCODER_SERVICE

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

    return VIDEO_ENCODER_SERVICE


def process_video_queue():
    video_encoder_service = __init_classes()

    video_encoder_service.encode_fifo()


def encode_video(video_queue_id: str):
    video_encoder_service = __init_classes()

    video_encoder_service.encode(video_queue_id)
