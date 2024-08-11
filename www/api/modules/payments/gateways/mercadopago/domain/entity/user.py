from dataclasses import dataclass


@dataclass
class User:
    id: str
    email: str

    @staticmethod
    def from_dict(user: dict):
        return User(
            id=user.get('id'),
            email=user.get('email'),
        )
