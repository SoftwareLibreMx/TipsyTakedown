import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from api.shared.infraestructure.utils import validate_dict, VKOptions, TrackTimeMixin, SoftDeleteMixin

Base = declarative_base()


class VideoModel(Base, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'videos'

    id: Mapped[str] = mapped_column(primary_key=True)
    teacher_id: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column()
    is_file_encoded: Mapped[bool] = mapped_column()

    @staticmethod
    def from_dict(data: dict) -> list:
        errors = validate_dict(data, [
            VKOptions('teacher_id', str, True),
            VKOptions('name', str, True),
            VKOptions('description', str, True),
        ])

        if errors:
            return errors, None

        return None, VideoModel(
            id=uuid.uuid4(),
            teacher_id=data.get('teacher_id'),
            name=data.get('name'),
            description=data.get('description'),
            is_file_encoded=data.get('isFileEncoded', False),
        )
