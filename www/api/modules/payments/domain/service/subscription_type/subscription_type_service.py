from typing import List, Optional

from ...dto.subscription_type_dto import SubscriptionTypeDTO
from ....infraestructure.repository.subscription_type import SubscriptionTypeRepository


class SubscriptionTypeService:
    def __init__(self, repository: SubscriptionTypeRepository):
        self.repository = repository

    def get(
            self, subscription_type_id: int) -> tuple[List[str], Optional[SubscriptionTypeDTO]]:
        subscription_type = self.repository.get(subscription_type_id)
        if not subscription_type:
            return ['Subscription type not found'], None

        return None, SubscriptionTypeDTO.from_entity(subscription_type)

    def get_all(self):

        subs_type_db = self.repository.get_all()
        subscription_types = []
        for sub_type in subs_type_db:
            subscription_types.append(sub_type._asdict())

        return subscription_types
