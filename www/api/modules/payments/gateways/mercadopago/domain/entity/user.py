from dataclasses import dataclass

from ..dto import Card


@dataclass
class User:
    id: str
    email: str
    cards: Card

    @staticmethod
    def from_dict(user: dict):
        return User(
            id=user.get('id'),
            email=user.get('email'),
            cards=user.get('cards')
        )
