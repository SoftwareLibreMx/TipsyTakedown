# here will be all the normal Crud applications
from shared.globals import db_engine
from ..domain.service import VideoService
from ..infraestructure.repository import VideoRepository


def __init_classes() -> [VideoRepository, VideoService]:
    video_repository = VideoRepository(db_engine)

    return [
        video_repository, VideoService(video_repository)
    ]


def get_video_by_id(video_id):
    _, video_service = __init_classes()

    return video_service.get_video_url(video_id)
