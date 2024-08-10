import mercadopago

from shared.globals import mercadopago_credentials


class CardRepository:
    def __init__(self):
        access_token = mercadopago_credentials.get('access_token', '')
        if not access_token:
            raise Exception('To use mercadopago you need accesstoken')

        self.sdk = mercadopago.SDK(access_token)

    def get_user_by_email(self, user_email):
        response = self.sdk.customer().search(filters={
            "email": user_email
        }).get('response', {})

        for user in response.get('results', []):
            return user

    def create_user(self, user_email):
        response = self.sdk.customer().create({
            "email": user_email
        }).get('response', {})

        return response

    def create_card(self, user_id, card):
        response = self.sdk.customer().create(user_id, {
            "token":  card.token,
            "issuer_id": card.issuer_id,
            "payment_method_id": card.payment_method_id
        }).get('response', None)

        return response
