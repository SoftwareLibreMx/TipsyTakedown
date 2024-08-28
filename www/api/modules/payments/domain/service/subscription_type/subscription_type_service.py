from typing import List, Optional

from ...dto.subscription_type_dto import SubscriptionTypeDTO
from ....infraestructure.repository.subscription_type import SubscriptionTypeRepository


class SubscriptionTypeService:
    def __init__(self, repository: SubscriptionTypeRepository):
        self.repository = repository

    def get(self, subscription_type_id: int) -> Optional[SubscriptionTypeDTO]:
        return self.repository.get(subscription_type_id)

    def get_all(self):

        subs_type_db = self.repository.get_all()
        subscription_types = []
        for sub_type in subs_type_db:
            subscription_types.append(sub_type._asdict())

        return subscription_types
