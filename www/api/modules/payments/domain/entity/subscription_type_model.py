from typing import Optional

from sqlalchemy import String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import (
    BaseModel,
    TrackTimeMixin,
    SoftDeleteMixin,
    validate_dict,
    VKOptions
)

from .currency import Currency
from .payment_cycle import PaymentCycle


class SubscriptionTypeModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'subscription_types'

    id: Mapped[str] = mapped_column(primary_key=True)
    payment_cycle: Mapped[PaymentCycle] = mapped_column(
        String(36), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[Currency] = mapped_column(
        String(3), nullable=False, default='MXN')
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True)

    @staticmethod
    def from_dict(
        data: dict
    ) -> tuple[Optional[list[str]], 'SubscriptionTypeModel']:
        errors = validate_dict(data, [
            VKOptions('payment_cycle', str, True),
            VKOptions('price', float, True),
            VKOptions('currency', str, False),
            VKOptions('is_active', bool, False)
        ])

        if errors:
            return errors, None

        return None, SubscriptionTypeModel(
            id=data.get('id', None),
            payment_cycle=data.get('payment_cycle', None),
            price=data.get('price', None),
            currency=data.get('currency', 'MXN'),
            is_active=data.get('is_active', True)
        )
