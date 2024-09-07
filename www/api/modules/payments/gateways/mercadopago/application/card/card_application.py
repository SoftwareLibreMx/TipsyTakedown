from typing import List

from api.modules.payments.domain.dto import SubscriptionTypeDTO
from api.modules.payments.domain.entity import CardModel

from ...domain.entity import User
from ...domain.service import CardService, UserService
from ...infrastructure.repository import CardRepository

CARD_REPOSITORY = None

USER_SERVICE = None
CARD_SERVICE = None


def __init_classes() -> CardService:
    global USER_SERVICE, CARD_SERVICE, CARD_REPOSITORY

    if CARD_REPOSITORY is None:
        CARD_REPOSITORY = CardRepository()

    if USER_SERVICE is None:
        USER_SERVICE = UserService()

    if CARD_SERVICE is None:
        CARD_SERVICE = CardService(USER_SERVICE, CARD_REPOSITORY)

    return CARD_SERVICE


def pay(
    req_user: dict,
    card: CardModel,
    subscription_type: SubscriptionTypeDTO,
) -> tuple[List[str], dict]:
    errors, user = User.from_dict(req_user)

    if errors:
        return errors, None

    card_service = __init_classes()

    return card_service.pay(user, card, subscription_type.price)
