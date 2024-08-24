from api.modules.admin.infrastructure.repository import MinioRepository


class MinioService:
    def __init__(self,
                 minio_repository: MinioRepository,
                 video_encodigs: list[str]):
        self.minio_repository = minio_repository
        self.video_encodings = video_encodigs

    def get_video_urls(self, video_id: str) -> list[str]:
        sign_urls = []
        for resolution in self.video_encodings:
            sign_urls.append(self.minio_repository.get_signed_url(
                f'{video_id}/{resolution}.mp4',
                60 * 60 * 24
            ))

        return sign_urls
