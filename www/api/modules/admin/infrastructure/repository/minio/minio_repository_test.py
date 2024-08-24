import unittest
from unittest import mock
from unittest.mock import patch, Mock

from api.libs.domain_entity import FlaskFile
from .minio_repository import MinioRepository, minio


class MinioS3RepositoryTest(unittest.TestCase):

    def setUp(self) -> None:
        self.endpoint = 'localhost:9000'
        self.access_key = 'minioadmin'
        self.secret_key = 'minioadmin'
        self.bucket_name = 'test'
        self.secure = False

    @patch.object(minio, 'Minio', Mock())
    def test_upload_flask_file(self):
        mock_minio = minio.Minio

        mock_put_object = Mock()
        mock_put_object.return_value = 'test'

        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_client.put_object = mock_put_object

        mock_minio.return_value = mock_client

        self.minio_s3_repository = MinioRepository(
            self.endpoint, self.access_key, self.secret_key, self.bucket_name, self.secure)

        object_key = 'test.txt'
        flask_file = FlaskFile(
            file_name='test.txt',
            content=b'test content',
            file_size=12,
            mimetype='text/plain'
        )

        self.minio_s3_repository.upload_flask_file(object_key, flask_file)

        mock_client.put_object.assert_called_once_with(
            self.bucket_name, object_key, mock.ANY, length=flask_file.file_size)
