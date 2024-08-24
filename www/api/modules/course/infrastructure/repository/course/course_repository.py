from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from ....domian.entity import CourseModel


class CourseRepository:
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def get_all(self, pagination=None):
        with Session(self.db_engine) as session:
            query = session.query(CourseModel)
            if pagination:
                query = query.limit(pagination.per_page).offset(
                    (pagination.page - 1) * pagination.per_page
                )

            return query.all()
