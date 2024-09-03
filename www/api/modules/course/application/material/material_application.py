from shared.globals import db_engine

from ...domian.service import MaterialService, MinioService
from ...infrastructure.repository import MaterialRepository

MINIO_SERVICE = None
MATERIAL_REPOSITORY = None
MATERIAL_SERVICE = None


def __init_classes() -> MaterialService:
    global MINIO_SERVICE, MATERIAL_REPOSITORY
    global MATERIAL_SERVICE

    if MATERIAL_SERVICE:
        return MATERIAL_SERVICE

    if not MINIO_SERVICE:
        MINIO_SERVICE = MinioService()

    if MATERIAL_REPOSITORY is None:
        MATERIAL_REPOSITORY = MaterialRepository(db_engine)

    MATERIAL_SERVICE = MaterialService(MATERIAL_REPOSITORY, MINIO_SERVICE)

    return MATERIAL_SERVICE


def get_all(filters: dict, pagination: dict) -> tuple[list[str], list[dict]]:
    material_service = __init_classes()

    return material_service.get_all(filters, pagination)
