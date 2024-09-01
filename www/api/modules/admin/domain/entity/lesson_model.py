import uuid

from sqlalchemy import ARRAY, Boolean, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import (
    BaseModel,
    TrackTimeMixin,
    SoftDeleteMixin,
)


class LessonModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'lessons'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    materials: Mapped[list[str]] = mapped_column(ARRAY(UUID), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True)
