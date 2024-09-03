from api.modules.payments.domain.dto import SubscriptionTypeDTO
from api.modules.payments.domain.entity import CardModel


class CardService:
    def __init__(self, card_repository):
        self.card_repository = card_repository

    def pay(
        self,
        req_user,
        req_card: CardModel,
        subscription_type: SubscriptionTypeDTO
    ) -> tuple[list[str], dict]:
        error, card_token = self.card_repository.generate_card_token(req_card)

        if error:
            return error, None

        return self.card_repository.pay_subscription({
            "amount": subscription_type.price,
            "currency": subscription_type.currency,
            "description": f"Initial payment for {req_user.email}",
            "source": card_token.get('id'),
        })
