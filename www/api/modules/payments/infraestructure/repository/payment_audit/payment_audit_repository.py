from sqlalchemy.orm import Session

from ....domain.entity import PaymentAuditModel


class PaymentAuditRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def create(self, payment_audit: PaymentAuditModel) -> PaymentAuditModel:
        with Session(self.db_engine) as session:
            session.add(payment_audit)
            session.commit()
            session.refresh(payment_audit)
            return payment_audit

    def update(self, video_id: str,
               payment_audit_dict: dict) -> PaymentAuditModel:
        with Session(self.db_engine) as session:
            payment_audit = session.query(PaymentAuditModel).filter_by(
                id=video_id, deleted_at=None).first()

            if not payment_audit:
                return ["Payment Audit not found"], None

            payment_audit.user_id = payment_audit_dict.get(
                'user_id', payment_audit.user_id)
            payment_audit.payment_amount = payment_audit_dict.get(
                'payment_amount', payment_audit.payment_amount)
            payment_audit.currency = payment_audit_dict.get(
                'currency', payment_audit.currency)
            payment_audit.transaction_date = payment_audit_dict.get(
                'transaction_date', payment_audit.transaction_date)
            payment_audit.status = payment_audit_dict.get(
                'status', payment_audit.status)
            payment_audit.rejection_reason = payment_audit_dict.get(
                'rejection_reason', payment_audit.rejection_reason)
            payment_audit.error = payment_audit_dict.get(
                'error', payment_audit.error)
            payment_audit.payment_method = payment_audit_dict.get(
                'payment_method', payment_audit.payment_method)
            payment_audit.card_id = payment_audit_dict.get(
                'card_id', payment_audit.card_id)

            session.commit()
            # session.refresh(payment_audit)
            return payment_audit
