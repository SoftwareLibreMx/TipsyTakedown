import bcrypt

from shared.globals import mercadopago_credentials as mp_credentials

from api.modules.payments.domain.dto import Subscription

from ...entity import User
from ...dto import Card


class CardService:
    def __init__(self, mp_card_repository, payment_audit_repo):
        self.salt = mp_credentials['hidde_user_email_salt']
        self.mp_repository = mp_card_repository
        self.payment_audit_repo = payment_audit_repo

    def pay_subscription(self, user: User,
                         req_card: Card, subscription: Subscription):
        encrypted_email = self.__get_encryptes_emaul(user.email)

        user = self.__get_or_create_user(encrypted_email)
        payment_card = self.__get_or_create_card(user, req_card)

        payment_audit = self.payment_audit_repo.create_payment_audit(
            user.id,
            payment_card.id,
            subscription,
        )

        response = self.mp_repository.pay_subscription({
            "transaction_amount": subscription.transaction_amount,
            "token": payment_card.card_token,
            "description": "",
            "payment_method_id": payment_card.payment_method_id,
            "installments": 1,
            "payer": {
                "email": encrypted_email
            }
        })

        self.payment_audit_repo.update_payment_audit(
            payment_audit.id, response['status'])

        return response

    def __get_encryptes_emaul(self, user_email):
        fake_domain = mp_credentials['fake_domain']
        encrypted_email = bcrypt.hashpw(
            user_email.encode('utf-8'), self.salt)
        return f'{encrypted_email.decode("utf-8")}@{fake_domain}'

    def __get_or_create_user(self, user_email):
        user = self.mp_repository.get_user_by_email(user_email)

        if not user:
            user = self.mp_repository.create_user(user_email)

        serialize_card = []
        for card in user.get('cards', []):
            serialize_card.append(Card.from_dict(card))

        serialize_user = User.from_dict(user)
        serialize_user.cards = serialize_card
        return serialize_user

    def __get_or_create_card(self, user, req_card):
        for mp_card in user.cards:
            if mp_card.last_four_digits == req_card.last_four_digits:
                return mp_card

        card = self.mp_repository.create_card(user.id, req_card)

        return Card.from_dict(card)
