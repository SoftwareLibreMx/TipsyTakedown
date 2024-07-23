from shared.globals import minion_credentials
from api.libs.domain_entity import FlaskFile

from ..infraestructure.repository import MinioS3Repository

s3_repository = None


def __init_classes() -> MinioS3Repository:
    s3_repository = globals().get('s3_repository')

    if s3_repository is None:
        s3_repository = MinioS3Repository(
            minion_credentials.get('endpoint'),
            minion_credentials.get('access_key'),
            minion_credentials.get('secret_key'),
            minion_credentials.get('bucket_name'),
            minion_credentials.get('secure')
        )

    return s3_repository


def upload_file(path: str, file: FlaskFile):
    s3_service = __init_classes()

    return s3_service.upload_flask_file(path, file)
