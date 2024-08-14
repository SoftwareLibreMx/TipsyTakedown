from typing import Optional

from sqlalchemy.orm import Session

from ....domain.entity import UserModel


class UserRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get_by_id(self, user_id: str) -> Optional[UserModel]:
        with Session(self.db_engine) as session:
            return (
                session.query(UserModel).filter_by(
                    id=user_id, deleted_at=None).first()
            )

    def create(self, user: UserModel) -> tuple[Optional[str], UserModel]:
        try:
            with Session(self.db_engine) as session:
                session.add(user)
                session.commit()
                session.refresh(user)
                return None, user
        except Exception as e:
            return str(e), None
