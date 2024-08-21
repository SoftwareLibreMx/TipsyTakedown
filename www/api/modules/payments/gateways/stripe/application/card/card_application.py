from api.modules.payments.domain.dto import SubscriptionTypeDTO
from api.modules.payments.domain.entity import CardModel

from ...infrastructure.repository import CardRepository
from ...domain.service import CardService

CARD_REPOSITORY = None

CARD_SERVICE = None


def __init_classes() -> CardService:
    global CARD_SERVICE, CARD_REPOSITORY

    if not CARD_REPOSITORY:
        CARD_REPOSITORY = CardRepository()

    if not CARD_SERVICE:
        CARD_SERVICE = CardService(CARD_REPOSITORY)

    return CARD_SERVICE


def pay(
    user: dict,
    card: CardModel,
    subscription_type: SubscriptionTypeDTO,
) -> tuple[list[str], dict]:
    card_service = __init_classes()

    return card_service.pay(user, card, subscription_type)
