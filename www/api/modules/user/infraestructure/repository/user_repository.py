from datetime import datetime
from sqlalchemy.orm import Session

from api.modules.user.domain.entity import UserModel


class UserRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get_user_by_id(self, user_id: str) -> UserModel:
        with Session(self.db_engine) as session:
            return (
                session.query(UserModel).filter_by(id=user_id, deleted_at=None).first()
            )

    def create_user(self, user: UserModel) -> UserModel:
        with Session(self.db_engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def update_user(self, user_id: str, user_dict: dict) -> UserModel:
        with Session(self.db_engine) as session:
            user_db = (
                session.query(UserModel).filter_by(id=user_id, deleted_at=None).first()
            )

            user_db.type = user_dict.get("type", user_db.type)
            user_db.given_name = user_dict.get("given_name", user_db.given_name)
            user_db.surname = user_dict.get("surname", user_db.surname)
            user_db.avatar = user_dict.get("avatar", user_db.avatar)
            user_db.updated_at = datetime.now()

            session.commit()
            session.refresh(user_db)
            return user_db

    def delete_user(self, user_id: str) -> UserModel:
        with Session(self.db_engine) as session:
            user_db = (
                session.query(UserModel).filter_by(id=user_id, deleted_at=None).first()
            )

            if not user_db:
                raise Exception("User not found")

            user_db.soft_delete()
            session.commit()
            session.refresh(user_db)
            return user_db
