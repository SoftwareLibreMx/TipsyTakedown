from typing import Optional

from shared.globals import db_engine

from ...domain.entity import SubscriptionModel
from ...domain.service import CardService, SubscriptionService
from ...infraestructure.repository import (
    CardRepository, PaymentAuditRepository, PromoRepository,
    SubscriptionRepository, SubscriptionTypeRepository
)

PAYMENT_AUDIT_REPOSITORY = None
PROMO_REPOSITORY = None
SUBSCRIPTION_REPOSITORY = None
SUBSCRIPTION_TYPE_REPOSITORY = None

CARD_REPOSITORY = None
CARD_SERVICE = None

SUBSCRIPTION_SERVICE = None


def __init_classes() -> None:
    global PAYMENT_AUDIT_REPOSITORY, PROMO_REPOSITORY, SUBSCRIPTION_REPOSITORY
    global SUBSCRIPTION_TYPE_REPOSITORY, CARD_REPOSITORY, CARD_SERVICE
    global SUBSCRIPTION_SERVICE

    if PAYMENT_AUDIT_REPOSITORY is None:
        PAYMENT_AUDIT_REPOSITORY = PaymentAuditRepository(db_engine)

    if PROMO_REPOSITORY is None:
        PROMO_REPOSITORY = PromoRepository(db_engine)

    if SUBSCRIPTION_REPOSITORY is None:
        SUBSCRIPTION_REPOSITORY = SubscriptionRepository(db_engine)

    if SUBSCRIPTION_TYPE_REPOSITORY is None:
        SUBSCRIPTION_TYPE_REPOSITORY = SubscriptionTypeRepository(db_engine)

    if CARD_REPOSITORY is None:
        CARD_REPOSITORY = CardRepository(db_engine)

    if CARD_SERVICE is None:
        CARD_SERVICE = CardService(CARD_REPOSITORY, PAYMENT_AUDIT_REPOSITORY)

    if SUBSCRIPTION_SERVICE is None:
        SUBSCRIPTION_SERVICE = SubscriptionService(
            CARD_SERVICE, PAYMENT_AUDIT_REPOSITORY, PROMO_REPOSITORY,
            SUBSCRIPTION_REPOSITORY, SUBSCRIPTION_TYPE_REPOSITORY
        )

    return SUBSCRIPTION_SERVICE


def pay_subscription(
    user: dict,
    subscription_type_id: str,
    payment_method: str,
    promo_code: Optional[str] = None,
    card: Optional[dict] = {},
) -> tuple[list[str], SubscriptionModel]:
    subscription_service = __init_classes()

    return subscription_service.pay(
        user, subscription_type_id, promo_code, payment_method, card
    )
