from dataclasses import dataclass


@dataclass
class Card:
    id: str
    last_four_digits: str
    card_token: str
    payment_method_id: str

    @staticmethod
    def from_dict(card: dict):
        return Card(
            id=card.get('id'),
            last_four_digits=card.get('last_four_digits'),
            card_token=card.get('card_token'),
            payment_method_id=card.get('payment_method_id')
        )
