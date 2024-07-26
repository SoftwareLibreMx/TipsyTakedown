import unittest
from unittest.mock import Mock, patch

from .video_uploader_service import VideoUploaderService

mock_video_eq_repo = Mock()
mock_video_file_repo = Mock()


class VideoUploaderServiceTest(unittest.TestCase):
    def setUp(self):
        self.video_uploader_service = VideoUploaderService(
            '', mock_video_eq_repo, mock_video_file_repo)

    def test_add_video_file_to_encoding_queue(self):
        mock_upload_flask_file = Mock()
        self.video_uploader_service.file_repository.upload_flask_file = mock_upload_flask_file

        video_id = '123'
        video_file = Mock()
        video_file.get_file_extension.return_value = 'mp4'

        self.video_uploader_service.add_video_file_to_encoding_queue(
            video_id, video_file)

        video_file.get_file_extension.assert_called_once()
        video_file.get_file_extension.assert_called
        mock_upload_flask_file.assert_called_once_with(
            f'/{video_id}.mp4', video_file)
        mock_video_eq_repo.create_encoding_queue.assert_called_once_with(
            video_id, '/123.mp4')
