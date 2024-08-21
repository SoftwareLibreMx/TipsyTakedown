import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import (
    BaseModel,
    TrackTimeMixin,
    SoftDeleteMixin,
    validate_dict,
    VKOptions
)


class SubscriptionModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'subscriptions'

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    subscription_type_id: Mapped[str] = mapped_column(String, nullable=False)
    payment_log_id: Mapped[str] = mapped_column(String, nullable=False)
    promo_code_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True)

    @staticmethod
    def from_dict(
        data: dict
    ) -> tuple[Optional[list[str]], 'SubscriptionModel']:
        errors = validate_dict(data, [
            VKOptions('user_id', str, True),
            VKOptions('subscription_type_id', str, True),
            VKOptions('payment_log_id', str, True),
            VKOptions('promo_code_id', str, False),
            VKOptions('start_date', datetime, True),
            VKOptions('end_date', datetime, True),
            VKOptions('is_active', bool, False)
        ])

        if errors:
            return errors, None

        return None, SubscriptionModel(
            id=data.get('id', uuid.uuid4()),
            **data
        )
