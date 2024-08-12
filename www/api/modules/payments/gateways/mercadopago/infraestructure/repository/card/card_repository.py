import mercadopago
from typing import Optional

from shared.globals import mercadopago_credentials

from api.modules.payments.domain.entity import Card


class CardRepository:
    def __init__(self):
        access_token = mercadopago_credentials.get('access_token', '')
        if not access_token:
            raise Exception('To use mercadopago you need accesstoken')

        self.sdk = mercadopago.SDK(access_token)

    def __print_error(self, response: dict):
        status = f"Status {response.get('status')}"
        error = f"error {response.get('cause', {})}"
        print(f"{status} {error}")

    def create_card_token(self, card: Card) -> Optional[dict]:
        response = self.sdk.card_token().create({
            "card_number": card.card_number,
            "security_code": card.security_code,
            "expiration_month": card.expiration_month,
            "expiration_year": card.expiration_year,
            "cardholder": {
                "name": card.cardholder_name,
            }
        }).get('response', None)

        if response.get('error', None):
            self.__print_error(response)
            return None

        return response

    def pay_subscription(self, data: dict) -> Optional[dict]:
        response = self.sdk.payment().create(data).get('response', None)

        if response.get('error', None):
            self.__print_error(response)
            return None

        return response
