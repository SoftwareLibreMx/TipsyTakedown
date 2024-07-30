# here will be all the normal Crud applications
from shared.globals import db_engine, minion_credentials

from ..domain.service import MinioService, VideoService
from ..infraestructure.repository import MinioRepository, VideoRepository
from ..domain.dto import VideoResponseDTO
from ..domain.entity import VideoModel

MINIO_REPOSITORY = None
VIDEO_REPOSITORY = None

MINIO_SERVICE = None
VIDEO_SERVICE = None


def __init_classes() -> VideoService:
    '''
    Didn't create service layer on crud because it was not necessary
    '''
    global MINIO_REPOSITORY, VIDEO_REPOSITORY, MINIO_SERVICE, VIDEO_SERVICE

    if VIDEO_SERVICE:
        return VIDEO_SERVICE

    if VIDEO_REPOSITORY is None:
        VIDEO_REPOSITORY = VideoRepository(db_engine)

    if MINIO_REPOSITORY is None:
        MINIO_REPOSITORY = MinioRepository(
            minion_credentials.get('endpoint'),
            minion_credentials.get('access_key'),
            minion_credentials.get('secret_key'),
            minion_credentials.get('bucket_name'),
            minion_credentials.get('secure')
        )

    if MINIO_SERVICE is None:
        MINIO_SERVICE = MinioService(MINIO_REPOSITORY)

    VIDEO_SERVICE = VideoService(VIDEO_REPOSITORY, MINIO_SERVICE)

    return VIDEO_SERVICE


def get_video_by_id(video_id) -> tuple[list[str], VideoResponseDTO]:
    video_service = __init_classes()

    return video_service.get_video_by_id(video_id)


def create_video(video_dict) -> tuple[list[str], VideoModel]:
    video_service = __init_classes()

    return video_service.create_video(video_dict)


def update_video(video_id, video_dict) -> tuple[list[str], VideoModel]:
    video_service = __init_classes()

    return video_service.update_video(video_id, video_dict)


def delete_video(video_id) -> tuple[list[str], VideoResponseDTO]:
    video_service = __init_classes()

    return video_service.delete_video(video_id)
