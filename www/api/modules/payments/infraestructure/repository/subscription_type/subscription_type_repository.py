class SubscriptionTypeRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get(self, subscription_type_id: str) -> dict:
        pass
