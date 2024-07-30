import os
import io
import minio

from minio.error import S3Error

from api.libs.domain_entity import FlaskFile


class MinioRepository:
    local_prefix = './tmp'

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

    def get_signed_url(self, object_key: str, expires: int) -> str:
        try:
            return self.client.presigned_get_object(
                self.bucket_name,
                object_key,
                expires=expires)
        except S3Error as exc:
            print(exc)
            return exc
        except Exception as exc:
            raise exc

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

    def upload_tmp(self, file_key: str) -> None:
        file_path = f'{self.local_prefix}/{file_key}'

        try:
            self.client.fput_object(self.bucket_name, file_key, file_path)
        except S3Error as exc:
            print(exc)
            raise exc

    def download_tmp(self, file_key: str) -> bool:
        path = f'{self.local_prefix}/{file_key}'

        try:
            self.client.fget_object(self.bucket_name, file_key, path)
            return True
        except S3Error as exc:
            print(exc)
            return False

    def remove_tmp(self, file_key: str) -> None:
        file_path = f'{self.local_prefix}/{file_key}'

        try:
            os.remove(file_path)
        except Exception as exc:
            print(exc)
            raise exc
