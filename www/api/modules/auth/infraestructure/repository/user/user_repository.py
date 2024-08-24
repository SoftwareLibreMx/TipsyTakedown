from typing import Optional

from sqlalchemy.orm import Session

from api.libs.utils import process_filters

from ....domain.entity import UserModel


class UserRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get_by_id(self, user_id: str,
                  filters: Optional[dict] = None) -> Optional[UserModel]:
        with Session(self.db_engine) as session:
            query = session.query(UserModel).filter_by(
                id=user_id, deleted_at=None)

            if filters:
                query = process_filters(UserModel, query, filters)

            return query.first()

    def create(self, user: UserModel) -> tuple[Optional[str], UserModel]:
        try:
            with Session(self.db_engine) as session:
                session.add(user)
                session.commit()
                session.refresh(user)
                return None, user
        except Exception as e:
            return str(e), None
