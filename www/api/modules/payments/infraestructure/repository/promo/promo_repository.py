from sqlalchemy.orm import Session

from ....domain.entity import PromoCodeModel


class PromoRepository:
    def get_by_code(self, promo_code: str) -> PromoCodeModel:
        with Session(self.db_engine) as session:
            return session.query(PromoCodeModel).filter_by(
                code=promo_code, deleted_at=None).first()
