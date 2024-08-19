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
            self, user_cred_dict: dict) -> UserCredentialModel:
        errors, user_cred = UserCredentialModel.from_dict(user_cred_dict)

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

    def update(self, user_cred_id, updated_data):
        return self.user_credential_repository.update(
            user_cred_id, updated_data)

    def delete(self, user_cred_id):
        return self.user_credential_repository.delete(
            user_cred_id)
