from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine

from api.libs.domain.entity import CourseModel


class CourseRepository:
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def create(self, course: CourseModel):
        with Session(self.db_engine) as session:
            session.add(course)
            session.commit()
            session.refresh(course)
            return course
