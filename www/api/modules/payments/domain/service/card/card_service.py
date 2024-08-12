from typing import Optional

from ...entity import Card, PaymentAuditModel
from ....gateways.mercadopago.application import (
    card_payment as meli_card_payment
)
from ....infraestructure.repository import (
    CardRepository, PaymentAuditRepository
)


class CardService:
    def __init__(
        self,
        card_repository: CardRepository,
        payment_audit_repo: PaymentAuditRepository
    ):
        self.card_repository = card_repository
        self.payment_audit_repo = payment_audit_repo

        self.payment_gateways = [
            meli_card_payment
        ]

    # TODO: Implement encrypt and decrypt methods
    def _decrypt_card(self, card: Card) -> Card:
        return card

    def _encrypt_card(self, card: Card) -> Card:
        return card

    def pay(
        self,
        user: dict,
        payment_amount: float,
        payment_audit: PaymentAuditModel,
        card: dict
    ) -> tuple[list[str], dict]:
        card = self.get_or_create(user.get('id', None), card)
        self.payment_audit_repo.update(payment_audit.id, {
            'card_id': card.get('id', None)
        })

        for gateway in self.payment_gateways:
            errors, response = gateway.pay(
                user, card, payment_amount, payment_audit)

            if errors:
                return errors, None

            return None, response

        return ["No payment gateway available"], None

    def create(self, user_id: str, card: dict) -> tuple[list[str], dict]:
        card = self._encrypt_card(Card.from_dict(card))

        return self.card_repository.create(user_id, card)

    def get_by_last_four_digits(
        self,
        user_id: str,
        last_four_digits: str
    ) -> Optional[Card]:
        return self.card_repository.get(user_id, last_four_digits)

    def get_or_create(
        self, user_id: str, card: dict
    ) -> tuple[list[str], dict]:
        card = self.get_by_last_four_digits(
            user_id, card.get('last_four_digits', None)
        )

        if card:
            return None, card

        return self.create(user_id, card)
