from sqlalchemy.orm import Mapped, mapped_column

from api.shared.infraestructure.utils import TrackTimeMixin, SoftDeleteMixin, BaseModel


class VideoEncodingQueueModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'video_encoding_queue'

    id: Mapped[str] = mapped_column(primary_key=True)
    video_id: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
