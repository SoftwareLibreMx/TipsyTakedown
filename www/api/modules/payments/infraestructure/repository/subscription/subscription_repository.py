from sqlalchemy.orm import Session

from ....domain.entity import SubscriptionModel


class SubscriptionRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def create(self, subscription: SubscriptionModel) -> dict:
        with Session(self.db_engine) as session:
            session.add(subscription)
            session.commit()
            session.refresh(subscription)
            return subscription
