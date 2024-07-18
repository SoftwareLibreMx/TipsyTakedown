from ..infraestructure.repository import MinioS3Repository
from ..domain.service import S3Service

s3_repository = None
s3_service = None


def __init_classes() -> S3Service:
    s3_repository = globals().get('s3_repository')
    s3_service = globals().get('s3_service')

    if s3_repository is None:
        s3_repository = MinioS3Repository()

    if s3_service is None:
        s3_service = S3Service(s3_repository)

    return s3_service


def upload_file(path, file):
    s3_service = __init_classes()

    return s3_service.upload_file(path, file)
