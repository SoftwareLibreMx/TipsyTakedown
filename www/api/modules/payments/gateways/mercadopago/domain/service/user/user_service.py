import bcrypt

from shared.globals import mercadopago_credentials as mp_credentials

from ....infraestructure.repository import UserRepository
from ...entity import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.salt = mp_credentials.get('hidde_user_email_salt', '')

        self.user_repository = user_repository

    def get_or_create(self, user: User) -> tuple[list[str], User]:
        user.email = self.encrypt_email(user.email)

        errors, user_meli = self.user_repository.get_by_email(user.email)

        if errors:
            return errors, None

        if not user_meli:
            errors, user_meli = self.user_repository.create(user)

            if errors:
                return errors, None

        return User.from_dict(user_meli)

    def encrypt_email(self, email: str) -> str:
        fake_domain = mp_credentials.get('fake_domain', 'fake.com')
        encrypted_email = bcrypt.hashpw(
            email.encode('utf-8'),
            self.salt
        )

        return f'{encrypted_email.decode("utf-8")}@{fake_domain}'
