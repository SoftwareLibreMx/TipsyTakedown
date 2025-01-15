from typing import List, Optional

from api.libs.domain_entity import UserType

from ...dto.subscription_type_dto import SubscriptionTypeDTO
from ....infraestructure.repository.subscription_type import SubscriptionTypeRepository
from ...entity import SubscriptionTypeModel


class SubscriptionTypeService:
    __valid_user_types = [UserType.ADMIN.value]

    def __init__(self, repository: SubscriptionTypeRepository):
        self.repository = repository

    def get(
            self,
            subscription_type_id: int
    ) -> tuple[List[str], Optional[SubscriptionTypeDTO]]:
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

    def create(self,
               user,
               subscription_type_data: dict
               ):

        if user.get("user_type") not in self.__valid_user_types:
            return "User is not authorized to create a subscription type", None

        subscription_type_data.pop('id', None)
        error, subscription_type = SubscriptionTypeModel.from_dict(
            subscription_type_data)

        if error:
            return error, None

        try:
            subscription_type = self.repository.create(subscription_type)
        except Exception as e:
            return [str(e)], None

        if not subscription_type:
            return ['Failed to create subscription type'], None

        return None, subscription_type

    def get_payment_cycles(self):
        payment_cycles_enum = self.repository.get_payment_cycles()
        payment_cycles = [cycle.value for cycle in payment_cycles_enum]

        return payment_cycles
