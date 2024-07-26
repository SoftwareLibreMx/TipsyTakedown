import unittest
from unittest.mock import call, Mock

from api.modules.video.domain.entity import VideoEncodingQueueStatus
from api.modules.video.domain.service import VideoEncoderService


class TestVideoEncoderService(unittest.TestCase):
    veq_repository = Mock()
    ffmpeg_service = Mock()
    minio_repository = Mock()

    def setUp(self) -> None:
        self.video_encoder_service = VideoEncoderService(
            self.veq_repository, self.ffmpeg_service, self.minio_repository
        )

    def test_encode_fifo_not_found(self):
        self.veq_repository.get_first_video_to_encode.return_value = None

        self.video_encoder_service.encode_fifo()

        self.veq_repository.get_first_video_to_encode.assert_called_once()
        self.ffmpeg_service.encode.assert_not_called()

    def test_encode_fifo(self):
        self.veq_repository.get_first_video_to_encode.side_effect = [
            Mock(), None]

        self.video_encoder_service.encode_fifo()

        self.veq_repository.get_first_video_to_encode.assert_called()
        self.ffmpeg_service.encode.assert_called()

    def test_encode_by_id_not_found(self):
        self.veq_repository.get_by_id.return_value = None

        self.video_encoder_service.encode_by_id('id')

        self.veq_repository.get_by_id.assert_called_once_with('id')
        self.ffmpeg_service.encode.assert_not_called()

    def test_encode_by_id(self):
        self.veq_repository.get_by_id.return_value = Mock()

        self.video_encoder_service.encode_by_id('id')

        self.veq_repository.get_by_id.assert_called_once_with('id')
        self.ffmpeg_service.encode.assert_called()

    def test_encode_by_entity_no_download(self):
        video_to_encode = Mock()
        self.minio_repository.download_tmp.return_value = False

        self.video_encoder_service.encode_by_entity(video_to_encode)

        self.minio_repository.download_tmp.assert_called_once_with(
            video_to_encode.file_key
        )
        self.veq_repository.update_status.assert_called_once_with(
            video_to_encode.id, VideoEncodingQueueStatus.FAILED
        )
        self.ffmpeg_service.encode.assert_not_called()

    def test_encode_by_entity_encode_error(self):
        video_to_encode = Mock()
        self.minio_repository.download_tmp.return_value = True
        self.ffmpeg_service.encode.return_value.error = 'error'
        update_status_calls = [
            call(video_to_encode.id, VideoEncodingQueueStatus.ENCODING),
            call(video_to_encode.id, VideoEncodingQueueStatus.FAILED)
        ]

        self.video_encoder_service.encode_by_entity(video_to_encode)

        self.minio_repository.download_tmp.assert_called_once_with(
            video_to_encode.file_key
        )

        self.veq_repository.update_status.asset_has_calls(update_status_calls)
        self.ffmpeg_service.encode.assert_called()
        self.minio_repository.upload_tmp.assert_not_called()
        self.minio_repository.remove_tmp.assert_not_called()

    def test_encode_by_entity(self):
        video_to_encode = Mock()
        self.minio_repository.download_tmp.return_value = True
        self.ffmpeg_service.encode.return_value.error = None
        update_status_calls = [
            call(video_to_encode.id, VideoEncodingQueueStatus.ENCODING),
            call(video_to_encode.id, VideoEncodingQueueStatus.COMPLETED)
        ]

        self.video_encoder_service.encode_by_entity(video_to_encode)

        self.minio_repository.download_tmp.assert_called_once_with(
            video_to_encode.file_key
        )

        self.veq_repository.update_status.asset_has_calls(update_status_calls)
        self.ffmpeg_service.encode.assert_called()
        self.minio_repository.upload_tmp.assert_called()
        self.minio_repository.remove_tmp.assert_called()
