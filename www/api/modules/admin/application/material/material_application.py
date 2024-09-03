from shared.globals import db_engine, minion_credentials

from ...domain.service import MinioService, MaterialService
from ...domain.service.video_encoder import ENCODINGS

from ...infrastructure.repository import MinioRepository, MaterialRepository
from ...domain.dto import MaterialResponseDTO

MINIO_REPOSITORY = None
MATERIAL_REPOSITORY = None

MINIO_SERVICE = None
MATERIAL_SERVICE = None


def __init_classes() -> MaterialService:
    global MINIO_REPOSITORY, MATERIAL_REPOSITORY
    global MINIO_SERVICE, MATERIAL_SERVICE

    if MATERIAL_SERVICE:
        return MATERIAL_SERVICE

    if MATERIAL_REPOSITORY is None:
        MATERIAL_REPOSITORY = MaterialRepository(db_engine)

    if MINIO_REPOSITORY is None:
        MINIO_REPOSITORY = MinioRepository(
            minion_credentials.get('endpoint'),
            minion_credentials.get('access_key'),
            minion_credentials.get('secret_key'),
            minion_credentials.get('bucket_name'),
            minion_credentials.get('secure')
        )

    if MINIO_SERVICE is None:
        MINIO_SERVICE = MinioService(MINIO_REPOSITORY, ENCODINGS)

    MATERIAL_SERVICE = MaterialService(MATERIAL_REPOSITORY, MINIO_SERVICE)

    return MATERIAL_SERVICE


def search_by_name(query: str) -> tuple[list[str], MaterialResponseDTO]:
    material_service = __init_classes()

    return material_service.search_by_name(query)


def get_by_id(material_id: str) -> tuple[list[str], MaterialResponseDTO]:
    material_service = __init_classes()

    return material_service.get_by_id(material_id)


def create(material_dict: dict) -> tuple[list[str], MaterialResponseDTO]:
    material_service = __init_classes()

    return material_service.create(material_dict)


def update(material_id: str,
           material_dict: dict) -> tuple[list[str], MaterialResponseDTO]:
    material_service = __init_classes()

    return material_service.update(material_id, material_dict)


def delete(material_id: str) -> tuple[list[str], MaterialResponseDTO]:
    material_service = __init_classes()

    return material_service.delete(material_id)
