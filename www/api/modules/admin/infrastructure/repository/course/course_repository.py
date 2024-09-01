from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine

from api.libs.domain.entity import CourseModel
from api.libs.utils import process_filters


class CourseRepository:
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def create(self, course: CourseModel):
        with Session(self.db_engine) as session:
            session.add(course)
            session.commit()
            session.refresh(course)
            return course

    def get_by_id(self, course_id: str, filters: dict = None):
        with Session(self.db_engine) as session:
            base_query = session.query(CourseModel).filter_by(
                id=course_id, deleted_at=None)

            if filters:
                base_query = process_filters(CourseModel, base_query, filters)

            return base_query.first()

    def update(self, course_id: str, course: dict):
        with Session(self.db_engine) as session:
            course_db = session.query(CourseModel).get(course_id)

            course_db.name = course.get("name", course_db.name)
            course_db.description = course.get(
                "description", course_db.description)
            course_db.long_description = course.get(
                "long_description", course_db.long_description)
            course_db.thumbnail = course.get("thumbnail", course_db.thumbnail)
            course_db.teacher_id = course.get(
                "teacher_id", course_db.teacher_id)
            course_db.lessons = course.get("lessons", course_db.lessons)
            course_db.teaser_material_id = course.get(
                "teaser_material_id", course_db.teaser_material_id)
            course_db.is_active = course.get("is_active", course_db.is_active)

            session.commit()
            session.refresh(course_db)
            return course_db
