from dataclasses import dataclass

from ...entity import UserType


@dataclass
class UserCDTO:
    id: int
    user_type: UserType
    email: str
    given_name: str
    surname: str
    avatar: str

    @classmethod
    def from_uc(cls, user, user_credentials):
        return cls(
            id=user.id,
            user_type=user.type.value,
            email=user_credentials.email,
            given_name=user.given_name,
            surname=user.surname,
            avatar=user.avatar
        )
