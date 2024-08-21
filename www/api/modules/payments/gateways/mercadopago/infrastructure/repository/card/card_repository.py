import mercadopago
from typing import Optional

from shared.globals import mercadopago_credentials

from api.modules.payments.domain.entity import CardModel


class CardRepository:
    def __init__(self):
        access_token = mercadopago_credentials.get('access_token', '')
        if not access_token:
            raise Exception('To use mercadopago you need accesstoken')

        self.sdk = mercadopago.SDK(access_token)

    def create_card_token(
        self,
        card: CardModel
    ) -> tuple[Optional[dict], Optional[dict]]:
        expiration_month, expiration_year = card.expiration_date.split('/')

        response = self.sdk.card_token().create({
            "card_number": card.card_number,
            "security_code": card.cvv,
            "expiration_month": expiration_month,
            "expiration_year": f'20{expiration_year}',
            "cardholder": {
                "name": card.card_holder_name,
            }
        }).get('response', None)

        if response.get('error', None):
            return response, None

        return None, response

    def pay_subscription(self,
                         data: dict) -> tuple[Optional[dict], Optional[dict]]:
        response = self.sdk.payment().create(data).get('response', None)

        if response.get('error', None):
            return response, None

        return None, response

    def get_user_by_email(self,
                          email: str) -> tuple[Optional[dict], Optional[dict]]:
        filters = {
            'email': email
        }

        response = self.sdk.customer().search(filters).get('response', None)

        if response.get('error', None):
            return response, None

        user = None

        for user in response['results']:
            return None, user

        return None, user

    def create_user(self,
                    user: dict) -> tuple[Optional[dict], Optional[dict]]:
        response = self.sdk.customer().create({
            'email': user.get('email', None),
        }).get('response', None)

        if response.get('error', None):
            return response, None

        return None, response
