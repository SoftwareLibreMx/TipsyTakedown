import asyncio

from ...infraestructure.repository import VideoEncodingQueuRepository


class UploaderServide:
    def __init__(self, video_eq_repository: VideoEncodingQueuRepository):
        self.video_eq_repository = video_eq_repository

    async def add_video_file_to_encoding_queue(self, video_id, video_file):

        return True
