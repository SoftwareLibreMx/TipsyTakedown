from ...infraestructure.repository import MinioS3Repository


class S3Service:
    def __init__(self, s3_repository: MinioS3Repository):
        self.s3_repository = s3_repository

    def upload_file(self, object_key: str, file_stream) -> list[str]:
        pass
