from shared.globals import db_engine

from ...domain.service import (
    AuthService, UserService, UserCredentialService
)
from ...infraestructure.repository import (
    UserRepository, UserCredentialRepository
)

AUTH_SERVICE = None
USER_REPOSITORY = None
UC_REPOSITORY = None
UC_SERVICE = None
USER_SERVICE = None


def __init_classes() -> AuthService:
    global AUTH_SERVICE, USER_REPOSITORY, UC_SERVICE
    global UC_REPOSITORY, USER_SERVICE

    if not USER_REPOSITORY:
        USER_REPOSITORY = UserRepository(db_engine)

    if not UC_REPOSITORY:
        UC_REPOSITORY = UserCredentialRepository(db_engine)

    if not UC_SERVICE:
        UC_SERVICE = UserCredentialService(UC_REPOSITORY)

    if not USER_SERVICE:
        USER_SERVICE = UserService(UC_SERVICE, USER_REPOSITORY)

    if not AUTH_SERVICE:
        AUTH_SERVICE = AuthService(USER_SERVICE, UC_SERVICE)

    return AUTH_SERVICE


def sign_up(user_c_dict: dict) -> tuple[list[str], dict]:
    auth_service = __init_classes()

    return auth_service.sign_up(user_c_dict)
