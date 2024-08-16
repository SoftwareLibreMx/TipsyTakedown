import bcrypt
from typing import Optional

from shared.globals import mercadopago_credentials as mp_credentials

from api.modules.payments.domain.entity import CardModel, RejectionReason

from ....infraestructure.repository import CardRepository
from ...entity import User


class CardService:
    def __init__(self, mp_card_repository: CardRepository):
        self.salt = mp_credentials.get('hidde_user_email_salt', '')

        self.mp_repository = mp_card_repository

    def pay(
        self,
        req_user: User,
        req_card: CardModel,
        transaction_amount: float
    ) -> tuple[list[str], dict]:
        payment_method_id = self.__get_payment_method_id(
            req_card.card_number)

        if not payment_method_id:
            return ["Card number not valid"], None

        encrypted_email = self.__get_encryptes_email(req_user.email)

        error, card_token = self.mp_repository.create_card_token(req_card)
        if error:
            return self._get_error_dict(error), None

        error, response = self.mp_repository.pay_subscription({
            "transaction_amount": transaction_amount,
            "token": card_token.get('id'),
            "description": "",
            "payment_method_id": payment_method_id,
            "installments": 1,
            "payer": {
                "email": encrypted_email
            }
        })

        if error:
            return self._get_error_dict(error), None

        return [], response

    def _get_error_dict(self, error: dict) -> dict:
        cause = error.get('cause', [])

        status = f"Status {error.get('status')}"
        error = f"error {cause}"

        return {
            'error': f"{status} {error}",
            'rejection_reason': self._get_rejection_reason(cause)
        }

    def _get_rejection_reason(self, cause: list[dict]) -> RejectionReason:
        code_to_rr = {
            'E205': RejectionReason.INVALID_EXPIRATION_DATE.value,
        }

        for error in cause:
            return code_to_rr.get(
                error.get('code'),
                RejectionReason.UNKNOWN.value
            )

    def __get_encryptes_email(self, user_email: str) -> str:
        fake_domain = mp_credentials.get('fake_domain', 'fake.com')
        encrypted_email = bcrypt.hashpw(
            user_email.encode('utf-8'),
            self.salt
        )

        return f'{encrypted_email.decode("utf-8")}@{fake_domain}'

    def __get_payment_method_id(self, card_number: str) -> Optional[str]:
        return {
            '4': 'visa',
            '2': 'master',
            '5': 'master',
        }.get(card_number[0], None)
