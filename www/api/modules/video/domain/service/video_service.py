from ...infraestructure.repository import VideoRepository


class VideoService:
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository

    def get_video_url(self, video_id):
        return self.video_repository.get_video_by_id(video_id)
