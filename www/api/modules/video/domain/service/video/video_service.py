from ..minio import MinioService

from ....infraestructure.repository import VideoRepository

from ....domain.dto import VideoResponseDTO
from ....domain.entity import VideoModel


class VideoService:
    def __init__(self, video_repository: VideoRepository,
                 minio_service: MinioService):
        self.video_repository = video_repository
        self.minio_service = minio_service

    def get_video_by_id(self,
                        video_id: str) -> tuple[list[str], VideoResponseDTO]:
        video = self.video_repository.get_video_by_id(video_id)

        if not video:
            return ['Video not found'], None

        video_urls = None
        if video.is_file_encoded:
            video_urls = self.minio_service.get_video_urls(video.id)

        video_response = VideoResponseDTO.from_entity(video)
        video_response.urls = video_urls or []

        return None, video_response

    def create_video(self,
                     video_dict: dict) -> tuple[list[str], VideoResponseDTO]:
        errors, video = VideoModel.from_dict(video_dict)

        if errors:
            return errors, None

        video = self.video_repository.create_video(video)

        return None, VideoResponseDTO.from_entity(video)

    def update_video(self, video_id: str,
                     video_dict: dict) -> tuple[list[str], VideoResponseDTO]:
        video = self.video_repository.get_video_by_id(video_id)

        if not video:
            return ['Video not found'], None

        errors, video = VideoModel.from_dict(video_dict, video)

        if errors:
            return errors, None

        video = self.video_repository.update_video(video)

        return None, VideoResponseDTO.from_entity(video)

    def delete_video(self,
                     video_id: str) -> tuple[list[str], VideoResponseDTO]:
        video = self.video_repository.get_video_by_id(video_id)

        if not video:
            return ['Video not found'], None

        try:
            self.video_repository.delete_video(video)
        except Exception as e:
            return [str(e)], None

        return None, VideoResponseDTO.from_entity(video)
