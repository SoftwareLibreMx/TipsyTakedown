from datetime import datetime
from sqlalchemy.orm import Session

from api.libs.domain.entity import MaterialModel


class MaterialRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get_by_id(self, material_id: str) -> MaterialModel:
        with Session(self.db_engine) as session:
            return session.query(MaterialModel).filter_by(
                id=material_id, deleted_at=None).first()

    def create(self, material: MaterialModel) -> MaterialModel:
        with Session(self.db_engine) as session:
            session.add(material)
            session.commit()
            session.refresh(material)
            return material

    def search_by_name(self, query: str):
        with Session(self.db_engine) as session:
            return session.query(MaterialModel).filter(
                MaterialModel.name.ilike(f'%{query}%')).all()

    def update(self, material_id: str, material_dict: dict) -> MaterialModel:
        with Session(self.db_engine) as session:
            material_db = session.query(MaterialModel).filter_by(
                id=material_id, deleted_at=None).first()

            material_db.teacher_id = material_dict.get(
                'teacher_id', material_db.teacher_id)
            material_db.name = material_dict.get('name', material_db.name)
            material_db.description = material_dict.get(
                'description', material_db.description)
            material_db.updated_at = datetime.now()

            session.commit()
            session.refresh(material_db)
            return material_db

    def delete(self, material_id: str) -> MaterialModel:
        with Session(self.db_engine) as session:
            material_db = session.query(MaterialModel).filter_by(
                id=material_id, deleted_at=None).first()

            if not material_db:
                raise Exception('Material not found')

            material_db.soft_delete()
            session.commit()
            session.refresh(material_db)
            return material_db
