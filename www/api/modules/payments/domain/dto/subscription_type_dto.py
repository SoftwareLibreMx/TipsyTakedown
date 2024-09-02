from dataclasses import dataclass
from api.modules.payments.domain.entity import SubscriptionTypeModel


@dataclass
class SubscriptionTypeDTO:
    id: str
    name: str
    payment_cycle: str
    price: float
    currency: str
    is_active: bool

    @staticmethod
    def from_entity(subscription_type: SubscriptionTypeModel):
        return SubscriptionTypeDTO(
            id=subscription_type.id,
            name=subscription_type.name,
            payment_cycle=subscription_type.payment_cycle,
            price=subscription_type.price,
            currency=subscription_type.currency,
            is_active=subscription_type.is_active)
