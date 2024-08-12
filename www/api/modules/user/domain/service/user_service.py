from ...infraestructure.repository import UserRepository
from ..entity import UserModel

class UserService:
  def __init__(self, user_repository: UserRepository):
    self.user_repository = user_repository

  def get_user_by_id(self, user_id: str) -> UserModel:
    # Get user from the repository by id
    user = self.user_repository.get_user_by_id(user_id)
    return user

  def get_user_by_email(self, email: str) -> UserModel:
    # Get user from the repository by email
    user = self.user_repository.get_user_by_id(email)
    return user

  def create_user(self, user_dict: dict) -> UserModel:

    errors, user = UserModel.from_dict(user_dict)

    if errors:
      return errors, None
    
    user = self.user_repository.create_user(user)

    return None, user

  def update_user(self, user_id, updated_data):
    # Update user in the repository
    user = self.user_repository.update_user(user_id, updated_data)

    return user

  def delete_user(self, user_id):
    # Delete user from the repository
    self.user_repository.delete_user(user_id)