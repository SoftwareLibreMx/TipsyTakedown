from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class LessonRepository:
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def search_by_name(self, query: str):
        with Session(self.db_engine) as session:
            return session.execute(text('''
                SELECT name FROM lessons WHERE name LIKE :query
            '''), {'query': query}).fetchall()
