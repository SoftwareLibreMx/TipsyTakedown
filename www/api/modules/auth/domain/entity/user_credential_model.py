import uuid

from sqlalchemy.orm import Mapped, mapped_column

from api.libs.utils import validate_dict, VKOptions, TrackTimeMixin, SoftDeleteMixin, BaseModel

class UserCredentialModel(BaseModel, TrackTimeMixin, SoftDeleteMixin):
    __tablename__ = 'user_credentials'

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    sso_provider: Mapped[str] = mapped_column()
    openid: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column()
    password_salt: Mapped[str] = mapped_column()
    password_hash_params: Mapped[str] = mapped_column()

    @staticmethod
    def from_dict(data: dict) -> list:
        errors = validate_dict(data, [
            VKOptions('user_id', str, True),
            VKOptions('email', str, True),
        ])

        if errors:
            return errors, None

        return None, UserCredentialModel(
            id=uuid.uuid4(),
            user_id=data.get('user_id'),
            email=data.get('email'),
        )
    @staticmethod
    def from_dict_sso_provider(data: dict) -> list:
        errors = validate_dict(data, [
            VKOptions('user_id', str, True),
            VKOptions('email', str, True),
            VKOptions('sso_provider', str, True),
            VKOptions('openid', str, True),
        ])

        if errors:
            return errors, None

        return None, UserCredentialModel(
            id=uuid.uuid4(),
            user_id=data.get('user_id'),
            email=data.get('email'),
            sso_provider=data.get('sso_provider'),
            openid=data.get('openid'),
        )
