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

    def __decrypt_card(self, card: Card) -> Card:
        pass

    def __encrypt_card(self, card: Card) -> Card:
        pass

    def pay(self, user: dict, card: Card,
            amount: float, payment_audit: PaymentAuditModel):
        card = self.__decrypt_card(card)

        for gateway in self.payment_gateways:
            errors, response = gateway.pay(user, card, amount, payment_audit)

            if errors:
                return errors, None

            return None, response

        return ["No payment gateway available"], None

    def create(self, user_id: str, card: dict) -> Card:
        pass
