from typing import List

from api.modules.payments.domain.entity import Card

from ...domain.entity import User
from ...domain.service import CardService
from ...infraestructure.repository import CardRepository

CARD_SERVICE = None
CARD_REPOSITORY = None


def __init_classes() -> CardService:
    global CARD_SERVICE, CARD_REPOSITORY

    if CARD_REPOSITORY is None:
        CARD_REPOSITORY = CardRepository()

    if CARD_SERVICE is None:
        CARD_SERVICE = CardService(CARD_REPOSITORY)

    return CARD_SERVICE


def pay(
    req_user: dict,
    card: Card,
    transaction_amount: float
) -> tuple[List[str], dict]:
    errors, user = User.from_dict(req_user)

    if errors:
        return errors, None

    card_service = __init_classes()

    return card_service.pay_subscription(user, card, transaction_amount)
