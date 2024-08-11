import uuid
from typing import List
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import (
    BaseModel,
    TrackTimeMixin,
    SoftDeleteMixin,
    validate_dict,
    VKOptions
)

from .payment_method import PaymentMethod
from .payment_status import PaymentStatus
from .rejection_reason import RejectionReason


class PaymentAuditModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'payment_audit'

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    payment_amount: Mapped[float] = mapped_column(String(36), nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3), nullable=False, default='MXN')
    transaction_date: Mapped[str] = mapped_column(DateTime, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        PaymentStatus, default=PaymentStatus.PENDING.value)
    reject_reason: Mapped[RejectionReason] = mapped_column(
        RejectionReason, nullable=True)
    payment_method: Mapped[PaymentMethod] = mapped_column(
        PaymentMethod, nullable=False)
    card_id: Mapped[str] = mapped_column(String(36), nullable=True)

    @staticmethod
    def from_dict(data: dict) -> tuple[List[str], 'PaymentAuditModel']:
        errors = validate_dict(data, [
            VKOptions('user_id', str, True),
            VKOptions('payment_amount', float, True),
            VKOptions('transaction_date', datetime, True),
            VKOptions('payment_method', PaymentMethod, True),
        ])

        if errors:
            return errors, None

        return None, PaymentAuditModel(
            id=str(uuid.uuid4()),
            user_id=data.get('user_id', None),
            payment_amount=data.get('payment_amount', None),
            currency=data.get('currency', 'MXN'),
            status=data.get('status', PaymentStatus.PENDING.value),
            payment_method=data.get('payment_method', None),
            card_id=data.get('card_id', None)
        )
