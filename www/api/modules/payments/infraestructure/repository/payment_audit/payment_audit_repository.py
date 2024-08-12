from datetime import datetime

from sqlalchemy.orm import Session

from api.libs.utils import validate_dict, VKOptions

from ....domain.entity import (
    PaymentAuditModel, PaymentMethod,
    PaymentStatus, RejectionReason
)


class PaymentAuditRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def create(self, payment_audit: dict) -> PaymentAuditModel:
        with Session(self.db_engine) as session:
            payment_audit = PaymentAuditModel.from_dict(payment_audit)
            session.add(payment_audit)
            session.commit()
            return payment_audit

    def update(self, video_id: str, payment_audit: dict) -> PaymentAuditModel:
        with Session(self.db_engine) as session:
            payment_audit_db = session.query(PaymentAuditModel).filter_by(
                id=video_id, deleted_at=None).first()

            if not payment_audit_db:
                return ["Payment Audit not found"], None

            errors = validate_dict(payment_audit, [
                VKOptions('user_id', str, False),
                VKOptions('payment_amount', float, False),
                VKOptions('currency', str, False),
                VKOptions('transaction_date', datetime, False),
                VKOptions('status', PaymentStatus, False),
                VKOptions('reject_reason', RejectionReason, False),
                VKOptions('payment_method', PaymentMethod, False),
                VKOptions('card_id', str, False),
            ])

            if errors:
                return errors, None

            payment_audit_db.user_id = payment_audit.get(
                'user_id', payment_audit_db.user_id)
            payment_audit_db.payment_amount = payment_audit.get(
                'payment_amount', payment_audit_db.payment_amount)
            payment_audit_db.currency = payment_audit.get(
                'currency', payment_audit_db.currency)
            payment_audit_db.transaction_date = payment_audit.get(
                'transaction_date', payment_audit_db.transaction_date)
            payment_audit_db.status = payment_audit.get(
                'status', payment_audit_db.status)
            payment_audit_db.reject_reason = payment_audit.get(
                'reject_reason', payment_audit_db.reject_reason)
            payment_audit_db.payment_method = payment_audit.get(
                'payment_method', payment_audit_db.payment_method)
            payment_audit_db.card_id = payment_audit.get(
                'card_id', payment_audit_db.card_id)

            session.commit()
            session.refresh(payment_audit_db)
            return payment_audit_db
