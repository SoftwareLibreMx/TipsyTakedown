import os
import pyscrypt
import json

from typing import Any, Dict

from shared.globals import password_hash_params

from ...entity import UserCredentialModel
from ....infraestructure.repository import UserCredentialRepository


class UserCredentialService:
    def __init__(self, user_credential_repository: UserCredentialRepository):
        self.user_credential_repository = user_credential_repository

    def get_by_id(self, user_credential_id):
        return self.user_credential_repository.get_user_credential_by_id(
            user_credential_id
        )

    def get_by_email(self, email):
        return self.user_credential_repository.get_user_credential_by_email(
            email
        )

    def create(
            self, user_id: str, user_cred_dict: dict) -> UserCredentialModel:
        salt = self.__generate_salt()
        hashing_config = {
            'N': password_hash_params.get('hash_n'),
            'r': password_hash_params.get('hash_r'),
            'p': password_hash_params.get('hash_p'),
            'dkLen': password_hash_params.get('hash_dklen')
        }

        errors, user_cred = UserCredentialModel.from_dict({
            'email': user_cred_dict.get('email'),
            'user_id': str(user_id),
            'password_hash': self.__generate_hash(
                user_cred_dict.get('password'),
                salt,
                hashing_config
            ),
            'password_salt': salt,
            'password_hash_params': json.dumps(hashing_config)
        })

        if errors:
            return errors, None

        user_cred = self.user_credential_repository.create(user_cred)

        return None, user_cred

    def create_sso(
            self, user_cred_dict: dict) -> UserCredentialModel:
        errors, user_cred = UserCredentialModel.from_dict_sso_provider(
            user_cred_dict)

        if errors:
            return errors, None

        user_cred = self.user_credential_repository.create(
            user_cred)

        return None, user_cred

    def validate_password(self, email, password) -> tuple[list[str], str]:
        salt, hash_params = self.user_credential_repository.get_cred_by_email(
            email
        )

        if not salt:
            return ['Not found'], None

        password_hash = self.__generate_hash(
            password,
            bytes(salt),
            json.loads(hash_params)
        )

        user_cred_id = self.user_credential_repository.validate_password(
            email, password_hash)

        if not user_cred_id:
            return ['Invalid password'], None

        return None, user_cred_id

    def update(self, user_cred_id, updated_data):
        return self.user_credential_repository.update(
            user_cred_id, updated_data)

    def delete(self, user_cred_id):
        return self.user_credential_repository.delete(
            user_cred_id)

    def __generate_salt(self, n=32) -> bytes:
        return os.urandom(n)

    def __generate_hash(self, passwd: str, salt: bytes,
                        parameters: Dict[str, Any]) -> bytes:
        """ Generates hash by using pyscrypt library. """
        passwd = passwd.encode()
        return pyscrypt.hash(passwd, salt, **parameters)
