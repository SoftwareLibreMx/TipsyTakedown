import bcrypt

from shared.globals import mercadopago_credentials as mp_credentials

from api.modules.payments.domain.dto import Subscription
from api.modules.payments.domain.entity import Card

from ...entity import User


class CardService:
    def __init__(self, mp_card_repository, payment_audit_repo):
        self.salt = mp_credentials['hidde_user_email_salt']
        self.mp_repository = mp_card_repository
        self.payment_audit_repo = payment_audit_repo

    def pay_subscription(
        self,
        user: User,
        req_card: Card,
        subscription: Subscription
    ) -> tuple[list[str], dict]:
        encrypted_email = self.__get_encryptes_emaul(user.email)

        user = self.__get_or_create_user(encrypted_email)
        if not user:
            return ["Error creating user"], None

        card_token = self.mp_repository.create_card_token(
            user.id, req_card)
        if not card_token:
            return ["Error creating card"], None

        payment_method_id = self.__get_payment_method_id(
            req_card.card_number)
        if not payment_method_id:
            return ["Card number not valid"], None

        payment_audit = self.payment_audit_repo.create_payment_audit(
            user.id,
            card_token.get('last_four_digits'),
            subscription,
        )

        response = self.mp_repository.pay_subscription({
            "transaction_amount": subscription.transaction_amount,
            "token": card_token.get('id'),
            "description": "",
            "payment_method_id": payment_method_id,
            "installments": 1,
            "payer": {
                "email": encrypted_email
            }
        })

        self.payment_audit_repo.update_payment_audit(
            payment_audit.id, response['status'])

        return None, response

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

    def __get_payment_method_id(self, card_number):
        return {
            '4': 'visa',
            '2': 'master',
            '5': 'master',
        }.get(card_number[0], None)
