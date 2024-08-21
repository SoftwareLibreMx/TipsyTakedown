from sqlalchemy.orm import Session

from ....domain.entity import CardModel


class CardRepository:
    def __init__(self, db_engine) -> None:
        self.db_engine = db_engine

    def get_by_last_four_digits(
        self,
        user_id: str,
        last_four_digits: str
    ) -> tuple[list[str], CardModel]:
        with Session(self.db_engine) as session:
            return session.query(CardModel).filter_by(
                user_id=user_id,
                last_four_digits=last_four_digits,
            ).first()

    def create(
        self,
        card: CardModel
    ) -> CardModel:
        with Session(self.db_engine) as session:
            session.add(card)
            session.commit()
            session.refresh(card)
            return card
