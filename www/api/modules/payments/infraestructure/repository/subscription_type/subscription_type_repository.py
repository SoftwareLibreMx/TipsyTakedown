from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from typing import Optional

from ....domain.entity import SubscriptionTypeModel


class SubscriptionTypeRepository:
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def get(self,
            subscription_type_id: str) -> Optional[SubscriptionTypeModel]:
        with Session(self.db_engine) as session:
            return session.query(SubscriptionTypeModel).filter_by(
                id=subscription_type_id, deleted_at=None).first()

    def get_all(self):
        with Session(self.db_engine) as session:
            return session.execute(text('''
                SELECT name, payment_cycle, price, currency, is_active
                FROM subscription_types
                WHERE deleted_at IS NULL AND is_active = TRUE
            ''')).fetchall()
