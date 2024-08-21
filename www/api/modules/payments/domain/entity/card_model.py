import uuid
from typing import Optional

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import (
    BaseModel,
    TrackTimeMixin,
    SoftDeleteMixin,
    validate_dict,
    VKOptions
)


class CardModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'cards'

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    card_number: Mapped[str] = mapped_column(String, nullable=False)
    expiration_date: Mapped[str] = mapped_column(String, nullable=False)
    cvv: Mapped[str] = mapped_column(String, nullable=False)
    card_holder_name: Mapped[str] = mapped_column(String, nullable=False)
    zip_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_four_digits: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True)

    @staticmethod
    def from_dict(
        data: dict
    ) -> tuple[Optional[list[str]], 'CardModel']:
        errors = validate_dict(data, [
            VKOptions('user_id', str, True),
            VKOptions('card_number', str, True),
            VKOptions('expiration_date', str, True),
            VKOptions('cvv', str, True),
            VKOptions('card_holder_name', str, True),
            VKOptions('zip_code', str, False),
            VKOptions('country', str, False),
            VKOptions('is_active', bool, False)
        ])

        if errors:
            return errors, None

        data['last_four_digits'] = data.get('card_number', None)[-4:]

        return None, CardModel(
            id=uuid.uuid4(),
            **data
        )
