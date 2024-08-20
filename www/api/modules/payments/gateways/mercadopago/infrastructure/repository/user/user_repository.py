import mercadopago
from typing import Optional

from shared.globals import mercadopago_credentials

from ....domain.entity import User


class UserRepository:
    def __init__(self):
        access_token = mercadopago_credentials.get('access_token', '')
        if not access_token:
            raise Exception('To use mercadopago you need accesstoken')

        self.sdk = mercadopago.SDK(access_token)

    def get_by_email(self,
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

    def create(self, user: User) -> tuple[Optional[dict], Optional[dict]]:
        response = self.sdk.customer().create({
            'email': user.email
        }).get('response', None)

        print(response)

        if response.get('error', None):
            return response, None

        return None, response
