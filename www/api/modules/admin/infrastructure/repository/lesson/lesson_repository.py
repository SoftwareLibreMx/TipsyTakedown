from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from api.modules.admin.domain.entity import LessonModel


class LessonRepository:
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def create_all(self, lessons: list[LessonModel]):
        with Session(self.db_engine) as session:
            session.add_all(lessons)
            session.commit()

            for lesson in lessons:
                session.refresh(lesson)

            return lessons

    def search_by_name(self, query: str):
        with Session(self.db_engine) as session:
            return session.query(LessonModel).filter(
                LessonModel.name.ilike(f'%{query}%')).all()

    def get_by_ids(self, lesson_ids: list[str]):
        with Session(self.db_engine) as session:
            return session.query(LessonModel).filter(
                LessonModel.id.in_(lesson_ids)).all()

    def update(self, lesson: dict):
        with Session(self.db_engine) as session:
            lesson_db = session.query(LessonModel).get(lesson.get('id'))

            if not lesson_db:
                return None

            lesson_db.name = lesson.get('name', lesson_db.name)
            lesson_db.materials = lesson.get('materials', lesson_db.materials)
            lesson_db.is_active = lesson.get('is_active', lesson_db.is_active)

            session.commit()
            session.refresh(lesson_db)
            return lesson_db
