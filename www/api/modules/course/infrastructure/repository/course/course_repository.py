from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from api.libs.domain.entity import CourseModel, Pagination
from api.libs.utils import process_filters


class CourseRepository:
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def get_all(
        self,
        filters: Optional[dict] = None,
        pagination: Optional[Pagination] = None
    ):
        with Session(self.db_engine) as session:
            query = (session
                     .query(CourseModel)
                     .filter(CourseModel.deleted_at.is_(None))
                     .order_by(CourseModel.updated_at.desc())
                     )

            if filters:
                query = process_filters(CourseModel, query, filters)

            if pagination:
                query = query.limit(pagination.per_page).offset(
                    (pagination.page - 1) * pagination.per_page
                )

            return query.all()
