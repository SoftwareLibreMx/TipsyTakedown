# here will be all the normal Crud applications
from shared.globals import db_engine
from ..domain.service.user_service import UserService
from ..infraestructure.repository import UserRepository
from ..domain.entity import UserModel

USER_REPOSITORY = None
USER_SERVICE = None


def __init_classes() -> UserService:
    global USER_SERVICE, USER_REPOSITORY

    if not USER_REPOSITORY:
        USER_REPOSITORY = UserRepository(db_engine)

    if not USER_SERVICE:
        USER_SERVICE = UserService(USER_REPOSITORY)

    return USER_SERVICE


def get_user_by_id(user_id) -> UserModel:
    user_service = __init_classes()

    return user_service.get_by_id(user_id)


def get_user_by_email(email) -> UserModel:
    user_service = __init_classes()

    return user_service.get_by_email(email)


def create_user(user_dict) -> tuple[list[str], UserModel]:
    user_service = __init_classes()

    return user_service.create(user_dict)


def update_user(user_id, user_dict) -> tuple[list[str], UserModel]:
    user_service = __init_classes()

    return user_service.update(user_id, user_dict)


def delete_user(user_id) -> UserModel:
    user_service = __init_classes()

    return user_service.delete(user_id)
