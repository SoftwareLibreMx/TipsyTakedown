import unittest
from unittest.mock import Mock

from api.modules.video.domain.service.ffmpeg import FFMPEGService


class TestFFmpegService(unittest.TestCase):
    def setUp(self) -> None:
        self.ffmpeg_repository = Mock()

        self.ffmpeg_service = FFMPEGService(self.ffmpeg_repository)

    def test_encode_error(self):
        scale = 'scale'
        file_name = 'file_name'
        self.ffmpeg_repository.encode.return_value = 'error this is my error'
        resp = self.ffmpeg_service.encode(scale, file_name)

        self.ffmpeg_repository.encode.assert_called_once_with(
            scale=scale,
            file_name=file_name,
            file_output_path=f'./tmp/{file_name}_output_{scale}.mp4'
        )
        self.assertEqual(resp.error, 'this is my error')

    def test_encode(self):
        scale = 'scale'
        file_name = 'file_name'
        self.ffmpeg_repository.encode.return_value = 'resp'
        resp = self.ffmpeg_service.encode(scale, file_name)

        self.ffmpeg_repository.encode.assert_called_once_with(
            scale=scale,
            file_name=file_name,
            file_output_path=f'./tmp/{file_name}_output_{scale}.mp4'
        )
        self.assertEqual(self.ffmpeg_repository.encode.call_count, 1)

        self.assertEqual(
            resp.file_path,
            f'./tmp/{file_name}_output_{scale}.mp4')
        self.assertEqual(resp.stdout, 'resp')
        self.assertIsNone(resp.error)
