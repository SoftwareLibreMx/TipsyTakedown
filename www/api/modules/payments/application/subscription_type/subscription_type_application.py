from typing import Optional

from shared.globals import db_engine

# from ...domain.entity import SubscriptionTypeModel
from ...infraestructure.repository import SubscriptionTypeRepository
from ...domain.service.subscription_type import SubscriptionTypeService

from ...domain.dto import SubscriptionTypeDTO

SUBSCRIPTION_TYPE_REPOSITORY = None
SUBSCRIPTION_TYPE_SERVICE = None


def __init_classes() -> None:
    global SUBSCRIPTION_TYPE_REPOSITORY, SUBSCRIPTION_TYPE_SERVICE

    if SUBSCRIPTION_TYPE_REPOSITORY is None:
        SUBSCRIPTION_TYPE_REPOSITORY = SubscriptionTypeRepository(db_engine)

    if SUBSCRIPTION_TYPE_SERVICE is None:
        SUBSCRIPTION_TYPE_SERVICE = SubscriptionTypeService(
            SUBSCRIPTION_TYPE_REPOSITORY
        )

    return SUBSCRIPTION_TYPE_SERVICE


def get(subscription_type_id) -> Optional[SubscriptionTypeDTO]:
    subscription_type_service = __init_classes()

    return subscription_type_service.get(subscription_type_id)


def get_all() -> list[SubscriptionTypeDTO]:
    subscription_type_service = __init_classes()

    return subscription_type_service.get_all()
