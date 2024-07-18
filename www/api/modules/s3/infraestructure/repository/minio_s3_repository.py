from minio import Minio
from minio.error import S3Error


class MinioS3Repository:

    def __init__(self, access_key: str, secret_key: str, bucket_name: str):
        self.client = Minio(
            access_key=access_key,
            secret_key=secret_key)

        if not self.client.bucket_exists(bucket_name):
            raise Exception('Bucket Not found')

        self.bucket_name = bucket_name

    def upload_file(self, object_key: str, file_size: int,
                    file_stream) -> list[str]:
        try:
            self.client.put_object(
                self.bucket_name,
                object_key,
                file_stream,
                length=file_size)
        except S3Error as exc:
            print(exc)
            return exc
