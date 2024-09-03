from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from api.libs.domain.entity import MaterialModel, Pagination
from api.libs.utils import process_filters


class MaterialRepository:
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def get_all(
        self,
        filters: Optional[dict] = None,
        pagination: Optional[Pagination] = None
    ):
        with Session(self.db_engine) as session:
            query = session.query(MaterialModel)

            if filters:
                query = process_filters(MaterialModel, query, filters)

            if pagination:
                query = query.limit(pagination.per_page).offset(
                    (pagination.page - 1) * pagination.per_page)

            return query.all()
