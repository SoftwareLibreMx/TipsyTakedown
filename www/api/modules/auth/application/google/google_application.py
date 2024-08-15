from shared.globals import db_engine

from ...domain.service import (
    AuthService, GoogleService, UserService, UserCredentialService
)
from ...infraestructure.repository import (
    UserRepository, UserCredentialRepository
)

AUTH_SERVICE = None

USER_REPOSITORY = None
UC_REPOSITORY = None
UC_SERVICE = None
USER_SERVICE = None

GOOGLE_SERVICE = None


def __init_classes():
    global AUTH_SERVICE, USER_REPOSITORY, UC_SERVICE
    global UC_REPOSITORY, USER_SERVICE, GOOGLE_SERVICE

    if not AUTH_SERVICE:
        AUTH_SERVICE = AuthService()

    if not USER_REPOSITORY:
        USER_REPOSITORY = UserRepository(db_engine)

    if not UC_REPOSITORY:
        UC_REPOSITORY = UserCredentialRepository(db_engine)

    if not UC_SERVICE:
        UC_SERVICE = UserCredentialService(UC_REPOSITORY)

    if not USER_SERVICE:
        USER_SERVICE = UserService(UC_SERVICE, USER_REPOSITORY)

    if GOOGLE_SERVICE is None:
        GOOGLE_SERVICE = GoogleService(AUTH_SERVICE, USER_SERVICE)

    return GOOGLE_SERVICE


def get_or_create_user_token(user_info: dict):
    google_service = __init_classes()

    return google_service.get_or_create_user_token(user_info)
