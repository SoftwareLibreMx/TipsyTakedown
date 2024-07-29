import uuid

from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import TrackTimeMixin, SoftDeleteMixin, BaseModel

class UserModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4())
    type: Mapped[str] = mapped_column(default='STUDENT')
    given_name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    avatar: Mapped[str] = mapped_column()
