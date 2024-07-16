# here will be all the normal Crud applications
from shared.globals import db_engine
from ..infraestructure.repository import VideoRepository
from ..domain.entity import VideoModel

video_repository = None


def __init_classes() -> VideoRepository:
    '''
    Didn't create service layer on crud because it was not necessary
    '''
    video_repository = globals().get('video_repository')

    if video_repository is None:
        video_repository = VideoRepository(db_engine)

    return video_repository


def get_video_by_id(video_id):
    video_repository = __init_classes()

    return video_repository.get_video_url(video_id)


def create_video(video_dict) -> tuple[list[str], VideoModel]:
    video_repository = __init_classes()

    errors, video = VideoModel.from_dict(video_dict)

    if errors:
        return errors, None

    return None, video_repository.create_video(video)
