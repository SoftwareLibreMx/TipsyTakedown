from typing import Optional

from ..user_credential_service import UserCredentialService

from ...dto import UserCDTO
from ...entity import UserModel

from ....infraestructure.repository import UserRepository


class UserService:
    def __init__(
        self,
        uc_service: UserCredentialService,
        user_repository: UserRepository
    ):
        self.user_repository = user_repository
        self.uc_service = uc_service

    def get_by_email(self, email) -> Optional[UserCDTO]:
        user_credentials = self.uc_service.get_by_email(email)

        if not user_credentials:
            return None

        user = self.user_repository.get_by_id(
            user_credentials.user_id)

        return UserCDTO.from_uc(user, user_credentials)

    def create(self, user_info: dict) -> tuple[Optional[str], UserModel]:
        error, user_model = UserModel.from_dict(user_info)

        if error:
            return error, None

        return self.user_repository.create(user_model)

    def create_sso(
        self,
        user_info: dict,
        sso_provider
    ) -> tuple[Optional[str], UserCDTO]:
        error, user_model = UserModel.from_dict(user_info)
        if error:
            return error, None

        error, user = self.user_repository.create(user_model)

        if error:
            return error, None

        error, user_cred = self.uc_service.create_user_credential_sso({
            "user_id": str(user.id),
            "sso_provider": sso_provider,
            "email": user_info.get("email", ""),
            "openid": user_info.get("openid", "")
        })

        if error:
            return error, None

        return None, UserCDTO.from_uc(user, user_cred)
