from api.libs.domain_entity import FlaskFile

from api.modules.admin.infrastructure.repository import (
    VideoEQRepository,
    MinioRepository
)


class VideoUploaderService:
    def __init__(self, key_prefix: str,
                 video_eq_repository: VideoEQRepository,
                 file_repository: MinioRepository):
        self.video_eq_repository = video_eq_repository
        self.prefix = key_prefix
        self.file_repository = file_repository

    def add_video_file_to_encoding_queue(
            self, video_id: str, video_file: FlaskFile):
        file_extension = video_file.get_file_extension()
        file_key = f'{self.prefix}/{video_id}.{file_extension}'

        # upload non encoded video to s3
        print('VUService: Start save not encode file')
        self.file_repository.upload_flask_file(file_key, video_file)
        print('VUService: not encode video saved')

        # create video encoding queue
        self.video_eq_repository.create_encoding_queue(video_id, file_key)
        print('VUService: Video added to encoding queue')
