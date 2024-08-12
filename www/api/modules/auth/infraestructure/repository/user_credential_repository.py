from datetime import datetime
from sqlalchemy.orm import Session

from api.modules.auth.domain.entity import UserCredentialModel

class UserCredentialRepository:
  def __init__(self, db_engine):
    self.db_engine = db_engine

  def get_user_credential_by_id(self, user_credential_id: str) -> UserCredentialModel:
    with Session(self.db_engine) as session:
      return session.query(UserCredentialModel).filter_by(
        id=user_credential_id, deleted_at=None).first()

  def get_user_credential_by_email(self, email: str) -> UserCredentialModel:
    with Session(self.db_engine) as session:
      return session.query(UserCredentialModel).filter_by(
        email=email, deleted_at=None).first()
    
  def create_user_credential(self, user_credential: UserCredentialModel) -> UserCredentialModel:
    with Session(self.db_engine) as session:
      session.add(user_credential)
      session.commit()
      session.refresh(user_credential)
      return user_credential
  
  def update_user_credential(self, user_cred_id: str, user_cred_dict: dict) -> UserCredentialModel:
    with Session(self.db_engine) as session:
      user_credential_db = session.query(UserCredentialModel).filter_by(
        id=user_cred_id, deleted_at=None).first()

      user_credential_db.user_id = user_cred_dict.get(
          'user_id', user_credential_db.user_id)
      user_credential_db.email = user_cred_dict.get(
          'email', user_credential_db.email)
      user_credential_db.sso_provider = user_cred_dict.get(
          'sso_provider', user_credential_db.sso_provider)
      user_credential_db.openid = user_cred_dict.get(
          'openid', user_credential_db.openid)
      user_credential_db.password_hash = user_cred_dict.get(
          'password_hash', user_credential_db.password_hash)
      user_credential_db.password_salt = user_cred_dict.get(
          'password_salt', user_credential_db.password_salt)
      user_credential_db.password_hash_params = user_cred_dict.get(
          'password_hash_params', user_credential_db.password_hash_params)

      user_credential_db.updated_at = datetime.now()

      session.commit()
      session.refresh(user_credential_db)
      return user_credential_db
    
  def delete_user_credential(self, user_cred_id: str) -> UserCredentialModel:
    with Session(self.db_engine) as session:
      user_credential_db = session.query(UserCredentialModel).filter_by(
          id=user_cred_id, deleted_at=None).first()

      if not user_credential_db:
          raise Exception('User Credential not found')

      user_credential_db.soft_delete()
      session.commit()
      session.refresh(user_credential_db)
      return user_credential_db
