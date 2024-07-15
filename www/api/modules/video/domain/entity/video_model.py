from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class VideoModel(DeclarativeBase):
    __tableanme__ = 'videos'

    id: Mapped[str] = mapped_column(primary_key=True)
    teacher_id: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column()
    updated_at: Mapped[DateTime] = mapped_column()
    deleted_at: Mapped[DateTime] = mapped_column()
