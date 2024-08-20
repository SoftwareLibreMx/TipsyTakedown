from api.modules.payments.gateways.stripe.domain.card.card_model import CardModel

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
    transaction_amount: float,
) -> tuple[list[str], dict]:
    card_service = __init_classes()

    return card_service.pay(user, card, transaction_amount)
