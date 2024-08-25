import uuid

from sqlalchemy import ARRAY, Boolean, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from ...utils import (
    BaseModel,
    TrackTimeMixin,
    SoftDeleteMixin,
    validate_dict,
    VKOptions
)


class CourseModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'courses'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    teacher_id: Mapped[str] = mapped_column(String(36), nullable=False)
    lessons: Mapped[list[str]] = mapped_column(ARRAY(UUID), nullable=False)
    thumbnail: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    long_description: Mapped[str] = mapped_column(String(255), nullable=False)
    thumbnail: Mapped[str] = mapped_column(String(255), nullable=False)
    teaser_material_id: Mapped[str] = mapped_column(String(36), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True)

    @staticmethod
    def from_dict(data: dict) -> tuple[list[str], 'CourseModel']:
        errors = validate_dict(data, [
            VKOptions('name', str, True),
            VKOptions('teacher_id', str, True),
            VKOptions('lessons', list, True),
            VKOptions('thumbnail', str, True),
            VKOptions('description', str, True),
            VKOptions('long_description', str, True),
            VKOptions('teaser_material_id', str, False),
            VKOptions('is_active', bool, False),
        ])

        if errors:
            return errors, None

        return None, CourseModel(
            id=str(uuid.uuid4()),
            name=data.get('name'),
            teacher_id=data.get('teacher_id'),
            lessons=data.get('lessons'),
            thumbnail=data.get('thumbnail'),
            description=data.get('description'),
            long_description=data.get('long_description'),
            teaser_material_id=data.get('teaser_material_id'),
            is_active=data.get('is_active', True),
        )
