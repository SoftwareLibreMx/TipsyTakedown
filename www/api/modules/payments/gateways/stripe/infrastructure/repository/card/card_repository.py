import stripe
from typing import Optional

from api.modules.payments.domain.entity import CardModel


class CardRepository:
    def __init__(self):
        self.stripe = stripe

    def create_card_token(
        self,
        card: CardModel
    ) -> tuple[Optional[dict], Optional[dict]]:
        try:
            card_token = self.stripe.Token.create(
                    card={
                        'number': card.card_number,
                        'exp_month': card.expiration_month,
                        'exp_year': card.expiration_year,
                        'cvc': card.cvv
                        }
                    )
        except Exception as e:
            return {'error': str(e)}, None

        return None, card_token

    def pay_subscription(self,
                         data: dict) -> tuple[Optional[dict], Optional[dict]]:
        try:
            payment = self.stripe.PaymentIntent.create(data)
        except Exception as e:
            return {'error': str(e)}, None

        return None, payment
