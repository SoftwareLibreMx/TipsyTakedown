from api.modules.video.infraestructure.repository import (
    MinioRepository, VideoEQRepository
)


class MinioService:
    def __init__(self,
                 minio_repository: MinioRepository,
                 video_encoder_service: VideoEQRepository):
        self.minio_repository = minio_repository
        self.video_encoder_service = video_encoder_service

    def get_video_urls(self, video_id: str) -> list[str]:
        sign_urls = []
        for resolution in self.video_encoder_service.encodings:
            sign_urls.append(self.minio_repository.get_signed_url(
                f'{video_id}/{resolution}.mp4'
            ))

        return sign_urls
