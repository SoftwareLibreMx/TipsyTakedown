from typing import Optional
from ..auth import AuthService
from ..user import UserService

from ...entity import SSOProvider


class GoogleService:
    def __init__(self, auth_service: AuthService, user_service: UserService):
        self.auth_service = auth_service
        self.user_service = user_service

    def get_or_create_user_token(self, user_info) -> Optional[dict]:
        user = self.user_service.get_by_email(
            user_info.get("email", ""))

        if not user:
            errors, user = self.user_service.create_sso(
                user_info, sso_provider=SSOProvider.GOOGLE.value)

            if errors:
                return errors, None

        return None, {
            "user": user,
            "token": self.auth_service.generate_token(user)
        }
