from api.modules.video.domain.entity import Encoding, VideoEncodeStatus
from api.modules.video.domain.repository import (
    VideoEQRepository, FFMPEGRepository
)


class VideoEncodingService:
    encodings = [
        Encoding('1080p'),
        Encoding('720p'),
        Encoding('480p'),
    ]

    def __init__(self, veq_repository: VideoEQRepository,
                 ffmpeg_repository: FFMPEGRepository):
        self.veq_repository = veq_repository
        self.ffmpeg_repository = ffmpeg_repository

    def exec(self):
        video_to_encode = self.video_eq_repository.get_first_video_to_encode()

        while video_to_encode is not None:
            self.veq_repository.update_status(VideoEncodeStatus.ENCODING)
            try:
                for encoding in self.encodings:
                    self.ffmpeg_repository.encode(
                        video_to_encode.file_key, encoding)

                # Delete video_to_encode from queue
                # change status to 'encoded'
            except Exception as e:
                self.veq_repository.update_status(VideoEncodeStatus.ERROR)
                # Log error
                print(e)

            video_to_encode = self.veq_repository.get_first_video_to_encode()

    def ffmped_encode(self, file_key: str, encoding: Encoding):
        # Call ffmpeg to encode video
        pass
