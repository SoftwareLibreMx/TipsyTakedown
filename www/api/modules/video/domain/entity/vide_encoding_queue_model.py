import uuid

from sqlalchemy.orm import Mapped, mapped_column

from api.shared.infrastructure.utils import (
    TrackTimeMixin, SoftDeleteMixin, BaseModel)


class VideoEncodingQueueModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'video_encoding_queue'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4())
    video_id: Mapped[str] = mapped_column()
    file_key: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default='PENDING')
