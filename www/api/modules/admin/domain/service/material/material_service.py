from ..minio import MinioService

from api.modules.admin.infrastructure.repository import MaterialRepository

from api.modules.admin.domain.dto import MaterialResponseDTO
from api.modules.admin.domain.entity import MaterialModel, MaterialType


class MaterialService:
    def __init__(self, material_repository: MaterialRepository,
                 minio_service: MinioService):
        self.material_repository = material_repository
        self.minio_service = minio_service

    def get_by_id(self,
                  material_id: str) -> tuple[list[str], MaterialResponseDTO]:
        material = self.material_repository.get_by_id(material_id)

        if not material:
            return ['Material not found'], None

        material_response = MaterialResponseDTO.from_entity(material)
        material_response.urls = self._get_file_urls(material)

        return None, material_response

    def _get_file_urls(self, material: MaterialModel) -> list[str]:
        locations = {
            MaterialType.VIDEO.value: lambda: self.minio_service.get_video_urls(
                material.id),
            MaterialType.PDF.value: lambda: self.minio_service.get_pdf_urls(
                material.id),
        }

        return locations.get(material.material_type, lambda: [])()

    def create(self,
               material_dict: dict) -> tuple[list[str], MaterialResponseDTO]:
        errors, material = MaterialModel.from_dict(material_dict)

        if errors:
            return errors, None

        material = self.material_repository.create(material)

        return None, MaterialResponseDTO.from_entity(material)

    def update(self, material_id: str,
               material_dict: dict) -> tuple[list[str], MaterialResponseDTO]:
        material = self.material_repository.get_by_id(material_id)

        if not material:
            return ['Material not found'], None

        errors, material = MaterialModel.from_dict(material_dict, material)

        if errors:
            return errors, None

        material = self.material_repository.update(material)

        return None, MaterialResponseDTO.from_entity(material)

    def delete(self,
               material_id: str) -> tuple[list[str], MaterialResponseDTO]:
        material = self.material_repository.get_by_id(material_id)

        if not material:
            return ['Material not found'], None

        try:
            material = self.material_repository.delete(material)
        except Exception as e:
            return [str(e)], None

        return None, MaterialResponseDTO.from_entity(material)
