import io
import minio

from minio.error import S3Error

from api.shared.domain import FlaskFile


class MinioS3Repository:

    def __init__(self, endpoint: str, access_key: str,
                 secret_key: str, bucket_name: str, secure: bool):
        self.client = minio.Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure)

        if not self.client.bucket_exists(bucket_name):
            raise Exception('Bucket Not found')

        self.bucket_name = bucket_name

    def upload_flask_file(self, object_key: str,
                          flask_file: FlaskFile) -> None:
        flask_file_stream = io.BytesIO(flask_file.content)
        try:
            print(f'MS3Repo: Start uploading {object_key}')
            upload_output = self.client.put_object(
                self.bucket_name,
                object_key,
                flask_file_stream,
                length=flask_file.file_size)

            print(f'MS3Repo: Finish uploading {object_key}')
            print(f'MS3Repo: Output {upload_output}')
        except S3Error as exc:
            print(exc)
            return exc
        except Exception as exc:
            raise exc
