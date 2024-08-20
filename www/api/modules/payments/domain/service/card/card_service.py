from ...dto import SubscriptionTypeDTO
from ...entity import CardModel, PaymentAuditModel
from ....gateways.mercadopago.application import (
    card_payment as meli_card_payment
)
from ....gateways.stripe.application import card_payment as stripe_card_payment
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
            meli_card_payment,
            stripe_card_payment
        ]

    # TODO: Implement encrypt and decrypt methods
    def _decrypt_card(self, card: CardModel) -> CardModel:
        return card

    def _encrypt_card(self, card: CardModel) -> CardModel:
        return card

    def pay(
        self,
        user: dict,
        subscription_type: SubscriptionTypeDTO,
        payment_audit: PaymentAuditModel,
        card: dict
    ) -> tuple[list[str], dict]:
        if not card:
            return ["Card is required"], None

        error, card = self._get_card_from_dict(user, card)

        if error:
            return error, None

        errors, encrypted_card = self.get_or_create(user.get('id', None), card)

        if errors:
            return errors, None

        card = self._decrypt_card(encrypted_card)

        self.payment_audit_repo.update(payment_audit.id, {
            'card_id': card.id
        })

        for gateway in self.payment_gateways:
            errors, response = gateway.pay(
                user, card, subscription_type)

            if errors:
                return errors, None

            return None, response

        return ["No payment gateway available"], None

    def create(self, user_id: str,
               card: CardModel | dict) -> tuple[list[str], CardModel]:
        if isinstance(card, dict):
            card = self._get_card_from_dict(user_id, card)

        card = self._encrypt_card(card)

        try:
            card = self.card_repository.create(card)
        except Exception as e:
            return [str(e)], None

        return None, card

    def get_or_create(
        self, user_id: str, card: CardModel
    ) -> tuple[list[str], dict]:
        card_db = self.card_repository.get_by_last_four_digits(
            user_id, card.last_four_digits
        )

        if card_db:
            return None, card_db

        return self.create(user_id, card)

    def _get_card_from_dict(self, user: dict, card: dict) -> CardModel:
        return CardModel.from_dict({
            'user_id': user.get('id', None),
            'card_number': card.get('card_number', '').replace(' ', ''),
            'expiration_date': card.get('expiration_date', None),
            'cvv': card.get('cvv', None),
            'card_holder_name': card.get('card_holder_name', None),
            'zip_code': card.get('zip_code', None),
            'country': card.get('country', None),
        })
