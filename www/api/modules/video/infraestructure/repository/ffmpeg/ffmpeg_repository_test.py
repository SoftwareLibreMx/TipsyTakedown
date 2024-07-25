from .ffmpeg_repository import FFMPEGRepository


class TestFFMPEGRepository:

    def test_ffmpeg_repository(self):
        ffmpeg_repository = FFMPEGRepository()
        assert ffmpeg_repository is not None

    def test_encode(self):
        ffmpeg_repository = FFMPEGRepository()
        assert ffmpeg_repository.encode('1080', 'IMG_2524.MOV') is not None
        assert ffmpeg_repository.encode('720', 'IMG_2524.MOV') is not None
        assert ffmpeg_repository.encode('540', 'IMG_2524.MOV') is not None
