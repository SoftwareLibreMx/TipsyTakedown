import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import (
    validate_dict,
    VKOptions,
    TrackTimeMixin,
    SoftDeleteMixin,
    BaseModel
)

from .material_type import MaterialType


class MaterialModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'materials'

    id: Mapped[str] = mapped_column(primary_key=True)
    material_type: Mapped[MaterialType] = mapped_column(String)
    teacher_id: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    file_path: Mapped[str] = mapped_column()
    is_file_encoded: Mapped[bool] = mapped_column()

    @staticmethod
    def from_dict(data: dict) -> list:
        errors = validate_dict(data, [
            VKOptions('teacher_id', str, True),
            VKOptions('material_type', MaterialType, True),
            VKOptions('name', str, True),
            VKOptions('description', str, True),
        ])

        if errors:
            return errors, None

        return None, MaterialModel(
            id=uuid.uuid4(),
            teacher_id=data.get('teacher_id'),
            material_type=data.get('material_type'),
            name=data.get('name'),
            description=data.get('description'),
            is_file_encoded=data.get('isFileEncoded', False),
        )
