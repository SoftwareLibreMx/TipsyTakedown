from typing import Optional

from api.libs.domain_entity import Pagination
from api.libs.utils import as_dict
from api.modules.course.infrastructure.repository import MaterialRepository

from ..minio.minio_service import MinioService


class MaterialService:
    def __init__(
        self,
            material_repository: MaterialRepository,
            minio_service: MinioService
    ):
        self.material_repository = material_repository
        self.minio_service = minio_service

    def get_all(
        self,
        filters: dict,
        pagination: Optional[dict] = {'page': 1, 'per_page': 10}
    ):
        pagination = Pagination(**pagination)

        materials = self.material_repository.get_all(filters, pagination)

        materials = list(map(as_dict, materials))

        return None, materials
