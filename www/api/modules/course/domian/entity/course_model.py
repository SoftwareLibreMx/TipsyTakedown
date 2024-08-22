from sqlalchemy import String, Array, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import BaseModel, TrackTimeMixin, SoftDeleteMixin


class CourseModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    lessons: Mapped[list[str]] = mapped_column(Array, nullable=False)
    thumbnail: Mapped[str] = mapped_column(String(255), nullable=False)
    teaser_material_id: Mapped[str] = mapped_column(String(36), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
