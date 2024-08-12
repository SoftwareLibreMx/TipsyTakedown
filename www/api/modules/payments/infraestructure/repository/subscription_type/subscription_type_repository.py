from sqlalchemy.orm import Session
from typing import Optional

from ....domain.entity import SubscriptionTypeModel


class SubscriptionTypeRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get(self,
            subscription_type_id: str) -> Optional[SubscriptionTypeModel]:
        with Session(self.db_engine) as session:
            return session.query(SubscriptionTypeModel).filter_by(
                id=subscription_type_id, deleted_at=None).first()
