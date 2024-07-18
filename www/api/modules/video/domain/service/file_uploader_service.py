import asyncio

from ...infraestructure.repository import VideoEncodingQueuRepository
from ....s3 import upload_file


class FileUploaderService:
    def __init__(self, key_prefix: str,
                 video_eq_repository: VideoEncodingQueuRepository):
        self.video_eq_repository = video_eq_repository
        self.prefix = key_prefix

    def add_video_file_to_encoding_queue(self, video_id, video_file):
        # get mime type
        mime_type = video_file.content_type
        print(mime_type)

        # upload non encoded video to s3
        upload_file(f'{self.prefix}/{video_id}', video_file)

        # create video encoding queue
