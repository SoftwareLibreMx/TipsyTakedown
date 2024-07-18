import asyncio

from shared.globals import db_engine

from ..domain.service import FileUploaderService
from ..infraestructure.repository import VideoEncodingQueuRepository

file_service = None
video_eq_repository = None


def __init_classes() -> FileUploaderService:
    file_service = globals().get('file_service')
    video_eq_repository = globals().get('video_eq_repository')

    if video_eq_repository is None:
        video_eq_repository = VideoEncodingQueuRepository(db_engine)

    if file_service is None:
        file_service = FileUploaderService(
            'test_upload_video', video_eq_repository)

    return file_service


def add_video_file_to_encoding_queue(video_id: str, video_file):
    file_service = __init_classes()

    return file_service.add_video_file_to_encoding_queue(
        video_id, video_file)
