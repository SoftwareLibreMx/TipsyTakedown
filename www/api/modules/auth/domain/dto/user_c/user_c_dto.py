from dataclasses import dataclass

from ...entity import UserType, UserCredentialModel, UserModel


@dataclass
class UserCDTO:
    id: int
    user_type: UserType
    email: str
    given_name: str
    surname: str
    avatar: str
    sso_provider: str = None

    @classmethod
    def from_uc(cls, user: UserModel, user_credentials: UserCredentialModel):
        return cls(
            id=user.id,
            user_type=user.type.value,
            email=user_credentials.email,
            given_name=user.given_name,
            surname=user.surname,
            avatar=user.avatar,
            sso_provider=user_credentials.sso_provider
        )
