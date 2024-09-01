from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from api.modules.admin.domain.entity import LessonModel


class LessonRepository:
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def search_by_name(self, query: str):
        with Session(self.db_engine) as session:
            return session.query(LessonModel).filter(
                LessonModel.name.ilike(f'%{query}%')).all()

    def get_by_ids(self, lesson_ids: list[str]):
        with Session(self.db_engine) as session:
            return session.query(LessonModel).filter(
                LessonModel.id.in_(lesson_ids)).all()
