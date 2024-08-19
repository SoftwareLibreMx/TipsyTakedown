from shared.globals import db_engine

from ..domain.service.user_credential import UserCredentialService
from ..infraestructure.repository import UserCredentialRepository
from ..domain.entity import UserCredentialModel

USER_CREDENTIAL_REPOSITORY = None
USER_CREDENTIAL_SERVICE = None


def __init_classes() -> UserCredentialService:
    global USER_CREDENTIAL_SERVICE, USER_CREDENTIAL_REPOSITORY

    if not USER_CREDENTIAL_REPOSITORY:
        USER_CREDENTIAL_REPOSITORY = UserCredentialRepository(db_engine)

    if not USER_CREDENTIAL_SERVICE:
        USER_CREDENTIAL_SERVICE = UserCredentialService(
            USER_CREDENTIAL_REPOSITORY
        )

    return USER_CREDENTIAL_SERVICE


def get_user_credential_by_id(user_cred_id) -> UserCredentialModel:
    user_cred_service = __init_classes()

    return user_cred_service.get_by_id(user_cred_id)


def get_user_credential_by_email(email) -> UserCredentialModel:
    user_cred_service = __init_classes()

    return user_cred_service.get_by_email(email)


def create_user_credential(
    user_cred_dict
) -> tuple[list[str], UserCredentialModel]:
    user_cred_service = __init_classes()

    return user_cred_service.create(user_cred_dict)


def create_user_credential_sso(
    user_cred_dict
) -> tuple[list[str], UserCredentialModel]:
    user_cred_service = __init_classes()

    return user_cred_service.create_sso(user_cred_dict)


def update_user_credential(
    user_cred_id, user_cred_dict
) -> tuple[list[str], UserCredentialModel]:
    user_cred_service = __init_classes()

    return user_cred_service.update(user_cred_id, user_cred_dict)


def delete_user_credential(user_cred_id) -> UserCredentialModel:
    user_cred_service = __init_classes()

    return user_cred_service.delete(user_cred_id)
