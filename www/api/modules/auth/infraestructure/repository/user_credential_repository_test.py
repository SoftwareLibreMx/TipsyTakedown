import unittest
from unittest.mock import MagicMock
from www.api.modules.auth.infraestructure.repository.user_credential_repository import UserCredentialRepository

class UserCredentialRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.user_credential_repository = UserCredentialRepository()

    def test_create_user_credential(self):
        user_credential = {
            "username": "test_user",
            "password": "test_password"
        }
        created_user_credential = self.user_credential_repository.create_user_credential(user_credential)
        self.assertEqual(created_user_credential["username"], "test_user")
        self.assertEqual(created_user_credential["password"], "test_password")

    def test_get_user_credential(self):
        user_credential = self.user_credential_repository.get_user_credential("test_user")
        self.assertEqual(user_credential["username"], "test_user")
        self.assertEqual(user_credential["password"], "test_password")

    def test_update_user_credential(self):
        user_credential = {
            "username": "test_user",
            "password": "test_password"
        }
        self.user_credential_repository.update_user_credential = MagicMock(return_value=user_credential)
        updated_user_credential = self.user_credential_repository.update_user_credential(user_credential)
        self.assertEqual(updated_user_credential["username"], "test_user")
        self.assertEqual(updated_user_credential["password"], "test_password")

    def test_delete_user_credential(self):
        self.user_credential_repository.delete_user_credential = MagicMock(return_value=None)
        self.user_credential_repository.delete_user_credential("test_user")
        self.assertIsNone(self.user_credential_repository.get_user_credential("test_user"))
