import bcrypt

from shared.globals import mercadopago_credentials as mp_credentials


class UserService:
    def __init__(self):
        self.salt = mp_credentials.get('hidde_user_email_salt', '')

    def encrypt_email(self, email: str) -> str:
        fake_domain = mp_credentials.get('fake_domain', 'fake.com')
        encrypted_email = bcrypt.hashpw(
            email.encode('utf-8'),
            self.salt
        )

        return f'{encrypted_email.decode("utf-8")}@{fake_domain}'
