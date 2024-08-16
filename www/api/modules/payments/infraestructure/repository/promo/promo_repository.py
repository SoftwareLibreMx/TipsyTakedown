from sqlalchemy.orm import Session

from ....domain.entity import PromoCodeModel


class PromoRepository:
    def __init__(self, db_engine) -> None:
        self.db_engine = db_engine

    def get_by_code(self, promo_code: str) -> PromoCodeModel:
        with Session(self.db_engine) as session:
            return session.query(PromoCodeModel).filter_by(
                code=promo_code, deleted_at=None).first()
