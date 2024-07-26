import pytest
from .ffmpeg_repository import FFMPEGRepository


class TestFFMPEGRepository:

    def test_ffmpeg_repository(self):
        ffmpeg_repository = FFMPEGRepository()
        assert ffmpeg_repository is not None

    @pytest.mark.parametrize('scale, file_path, output_file_path', [
        ('1080', 'IMG_2524.MOV', 'IMG_2524_1080.mp4'),
        ('720', 'IMG_2524.MOV', 'IMG_2524_720.mp4'),
        ('540', 'IMG_2524.MOV', 'IMG_2524_540.mp4'),
    ])
    def test_encode(self, scale, file_path, output_file_path):
        ffmpeg_repository = FFMPEGRepository()

        assert ffmpeg_repository.encode(
            scale, file_path, output_file_path) is not None
