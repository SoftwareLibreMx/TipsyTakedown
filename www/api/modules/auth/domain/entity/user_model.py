import uuid

from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import (
    BaseModel,
    TrackTimeMixin,
    SoftDeleteMixin,
    validate_dict,
    VKOptions
)

from .user_type import UserType


class UserModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[UserType] = mapped_column(default=UserType.STUDENT.value)
    given_name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    avatar: Mapped[str] = mapped_column()

    @staticmethod
    def from_dict(data: dict) -> list:
        errors = validate_dict(data, [
            VKOptions("given_name", str, True),
            VKOptions("surname", str, True),
        ])

        if errors:
            return errors, None

        return None, UserModel(
            id=uuid.uuid4(),
            given_name=data.get("given_name"),
            surname=data.get("surname"),
            avatar=data.get("avatar"),
        )
