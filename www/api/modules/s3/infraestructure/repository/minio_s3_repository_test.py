import unittest
from unittest import mock
from unittest.mock import patch, Mock

from api.shared.domain import FlaskFile
from api.modules.s3.infraestructure.repository.minio_s3_repository import MinioS3Repository


class MinioS3RepositoryTest(unittest.TestCase):

    def setUp(self) -> None:
        self.endpoint = 'localhost:9000'
        self.access_key = 'minioadmin'
        self.secret_key = 'minioadmin'
        self.bucket_name = 'test'
        self.secure = False

    def test_upload_flask_file(self):
        mock_put_object = Mock()
        mock_put_object.return_value = 'test'

        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_client.put_object = mock_put_object

        mock_minio = patch(
            'api.modules.s3.infraestructure.repository.minio_s3_repository.Minio').start()
        mock_minio.return_value = mock_client

        self.minio_s3_repository = MinioS3Repository(
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
