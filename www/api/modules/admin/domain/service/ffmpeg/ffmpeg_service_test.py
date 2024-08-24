import unittest
from unittest.mock import Mock, patch

from api.modules.admin.domain.service.ffmpeg.ffmpeg_service import FFMPEGService, os


class TestFFmpegService(unittest.TestCase):
    def setUp(self) -> None:
        self.ffmpeg_repository = Mock()

        self.ffmpeg_service = FFMPEGService(self.ffmpeg_repository)

    @patch.object(os, 'makedirs', Mock())
    def test_encode_error(self):
        scale = 'scale'
        file_name = 'file_name'
        output_file_key = f'{file_name}_output_{scale}.mp4'
        self.ffmpeg_repository.encode.return_value = 'error this is my error'
        resp = self.ffmpeg_service.encode(scale, file_name, output_file_key)

        self.ffmpeg_repository.encode.assert_called_once_with(
            scale, f'./tmp/{file_name}', f'./tmp/{file_name}_output_{scale}.mp4'
        )
        self.assertEqual(resp.error, 'this is my error')

    @patch.object(os, 'makedirs', Mock())
    def test_encode(self):
        scale = 'scale'
        file_key = 'file_name'
        output_file_key = f'{file_key}_output_{scale}.mp4'
        self.ffmpeg_repository.encode.return_value = 'resp'
        resp = self.ffmpeg_service.encode(scale, file_key, output_file_key)

        self.ffmpeg_repository.encode.assert_called_once_with(
            scale, f'./tmp/{file_key}', f'./tmp/{output_file_key}'
        )
        self.assertEqual(self.ffmpeg_repository.encode.call_count, 1)

        self.assertEqual(
            resp.file_path,
            f'./tmp/{output_file_key}')
        self.assertEqual(resp.stdout, 'resp')
        self.assertIsNone(resp.error)
