from api.modules.video.domain.entity import (
    Encoding, VideoEncodingQueueStatus, VideoEncodingQueueModel
)

from api.modules.video.domain.service.ffmpeg import FFMPEGService

from api.modules.video.infraestructure.repository import (
    VideoEQRepository, MinioRepository
)


class VideoEncoderService:
    encodings = [
        Encoding('1080p'),
        Encoding('720p'),
        Encoding('480p'),
    ]

    def __init__(self, veq_repository: VideoEQRepository,
                 ffmpeg_service: FFMPEGService,
                 minio_repository: MinioRepository):
        self.veq_repository = veq_repository
        self.ffmpeg_service = ffmpeg_service
        self.minio_repository = minio_repository

    def encode_fifo(self):
        video_to_encode = self.veq_repository.get_first_video_to_encode()

        while video_to_encode is not None:
            self.encode_by_entity(video_to_encode)

            video_to_encode = self.veq_repository.get_first_video_to_encode()

    def encode_by_id(self, video_queue_id: str):
        video_to_encode = self.veq_repository.get_by_id(video_queue_id)

        if video_to_encode is None:
            return

        self.encode_by_entity(video_to_encode)

    def encode_by_entity(self, video_to_encode: VideoEncodingQueueModel):
        is_downloaded = self.minio_repository.download_tmp(
            video_to_encode.file_key
        )

        if not is_downloaded:
            self.veq_repository.update_status(
                video_to_encode.id, VideoEncodingQueueStatus.FAILED
            )
            return

        self.veq_repository.update_status(
            video_to_encode.id, VideoEncodingQueueStatus.ENCODING
        )

        errors = []
        for encoding in self.encodings:
            ffmpeg_encode = self.ffmpeg_service.encode(
                encoding, video_to_encode.file_key)

            if ffmpeg_encode.error is not None:
                errors.append(ffmpeg_encode.error)
                continue

            self.minio_repository.upload_tmp(ffmpeg_encode)
            self.minio_repository.remove_tmp(ffmpeg_encode.file_path)

        if errors:
            self.veq_repository.update_status(
                video_to_encode.id, VideoEncodingQueueStatus.FAILED
            )
            print(errors)
            return

        self.veq_repository.update_status(
            video_to_encode.id, VideoEncodingQueueStatus.COMPLETED
        )

        self.minio_repository.remove_tmp(video_to_encode.file_key)
