from shared.globals import db_engine
from ..infraestructure.repository import UserCredentialRepository
from ..domain.entity import UserCredentialModel

user_credential_repository = None


def __init_classes() -> UserCredentialRepository:

    user_credential_repository = globals().get("user_credential_repository")

    if user_credential_repository is None:
        user_credential_repository = UserCredentialRepository(db_engine)

    return user_credential_repository


def get_user_credential_by_id(user_cred_id):
    user_credential_repository = __init_classes()

    return user_credential_repository.get_user_credential_by_id


def create_user_credential(user_cred_dict) -> tuple[list[str], UserCredentialModel]:
    user_credential_repository = __init_classes()

    errors, user_credential = UserCredentialModel.from_dict(user_cred_dict)

    if errors:
        return errors, None

    return None, user_credential_repository.create_user_credential(user_credential)


def update_user_credential(
    user_cred_id, user_cred_dict
) -> tuple[list[str], UserCredentialModel]:
    user_credential_repository = __init_classes()

    return None, user_credential_repository.update_user_credential(user_cred_dict)


def delete_user_credential(user_cred_id) -> UserCredentialModel:
    user_credential_repository = __init_classes()

    try:
        user_credential_repository.delete_user_credential(user_cred_id)
    except Exception as e:
        return [str(e)]
