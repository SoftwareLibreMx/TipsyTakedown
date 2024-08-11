from dataclasses import dataclass
from typing import List

from api.libs.utils import validate_dict, VKOptions


@dataclass
class User:
    id: str
    email: str

    @staticmethod
    def from_dict(user: dict) -> tuple[List[str], "User"]:
        errors = validate_dict(user, [
            VKOptions('id', str),
            VKOptions('email', str),
        ])

        if errors:
            return errors, None

        return None, User(
            id=user.get('id'),
            email=user.get('email'),
        )
