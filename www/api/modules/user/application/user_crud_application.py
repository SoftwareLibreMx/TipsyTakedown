# here will be all the normal Crud applications
from shared.globals import db_engine
from ..infraestructure.repository import UserRepository
from ..domain.entity import UserModel

user_repository = None


def __init_classes() -> UserRepository:
    user_repository = globals().get('user_repository')

    if user_repository is None:
        user_repository = UserRepository(db_engine)

    return user_repository


def get_user_by_id(user_id):
    user_repository = __init_classes()

    return user_repository.get_user_by_id(user_id)


def create_video(user_dict) -> tuple[list[str], UserModel]:
    user_repository = __init_classes()

    errors, video = UserModel.from_dict(user_dict)

    if errors:
        return errors, None

    return None, user_repository.create_user(video)


def update_video(user_id, user_dict) -> tuple[list[str], UserModel]:
    user_repository = __init_classes()

    return None, user_repository.update_user(user_id, user_dict)


def delete_video(user_id) -> UserModel:
    user_repository = __init_classes()

    try:
        user_repository.delete_user(user_id)
    except Exception as e:
        return [str(e)]
