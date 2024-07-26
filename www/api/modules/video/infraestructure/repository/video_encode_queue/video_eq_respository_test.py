import unittest
from unittest.mock import Mock, patch, MagicMock

from api.modules.video.domain.entity import VideoEncodingQueueModel, VideoEncodingQueueStatus
from api.modules.video.infraestructure.repository import VideoEQRepository


class TestVideoEQRepository(unittest.TestCase):
    repo_location = 'api.modules.video.infraestructure.repository'
    mock_db_engine = Mock()

    def setUp(self):
        self.mock_session = patch(
            f'{self.repo_location}.video_encode_queue.video_eq_repository.Session',
        ).start()
        self.video_eq_repository = VideoEQRepository(self.mock_db_engine)

    def test_create_encoding_queue(self):
        video_encoding_queue = VideoEncodingQueueModel(
            video_id='test_video_id', file_key='test_file_key'
        )

        mock_session_instance = MagicMock()
        mock_session_instance.__enter__.return_value = mock_session_instance
        self.mock_session.return_value = mock_session_instance

        self.video_eq_repository.create_encoding_queue(
            video_id=video_encoding_queue.video_id, file_key=video_encoding_queue.file_key
        )

        self.mock_session.assert_called_once_with(self.mock_db_engine)
        mock_session_instance.add.assert_called_once()
        mock_session_instance.commit.assert_called_once()
        mock_session_instance.refresh.assert_called_once()

    def test_get_first_video_to_encode(self):
        video_encoding_queue = VideoEncodingQueueModel(
            video_id='test_video_id', file_key='test_file_key'
        )
        mock_session_instance = MagicMock()
        mock_session_instance.__enter__.return_value = mock_session_instance
        mock_session_instance.query.return_value = mock_session_instance
        mock_session_instance.filter_by.return_value = mock_session_instance
        mock_session_instance.first.return_value = video_encoding_queue

        self.mock_session.return_value = mock_session_instance

        resp = self.video_eq_repository.get_first_video_to_encode()

        self.mock_session.assert_called_once_with(self.mock_db_engine)
        mock_session_instance.query.assert_called_once()
        mock_session_instance.filter_by.assert_called_once()
        mock_session_instance.first.assert_called_once()

        self.assertEqual(resp, video_encoding_queue)

    def test_update_status(self):
        video_encoding_queue = VideoEncodingQueueModel(
            video_id='test_video_id', file_key='test_file_key'
        )
        mock_session_instance = MagicMock()
        mock_session_instance.__enter__.return_value = mock_session_instance
        mock_session_instance.query.return_value = mock_session_instance
        mock_session_instance.filter_by.return_value = mock_session_instance
        mock_session_instance.first.return_value = video_encoding_queue

        self.mock_session.return_value = mock_session_instance

        resp = self.video_eq_repository.update_status(
            video_id=video_encoding_queue.video_id, status=VideoEncodingQueueStatus.PENDING
        )

        self.mock_session.assert_called_once_with(self.mock_db_engine)
        mock_session_instance.query.assert_called_once()
        mock_session_instance.filter_by.assert_called_once()
        mock_session_instance.first.assert_called_once()
        mock_session_instance.commit.assert_called_once()
        mock_session_instance.refresh.assert_called_once_with(
            video_encoding_queue)

        self.assertEqual(resp, video_encoding_queue)
