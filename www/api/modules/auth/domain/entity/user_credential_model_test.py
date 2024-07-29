from .user_credential_model import UserCredentialModel
def test_from_dict():
  mock_user_dict = {
        'user_id': '123123123',
        'email': 'email@domain.com',
  }
  expected_user = UserCredentialModel(
    user_id='123123123',
    email = 'email@domain.com',
  )

  errors, user = UserCredentialModel.from_dict(mock_user_dict)

  assert errors is None

  assert user.user_id == expected_user.user_id
  assert user.email == expected_user.email