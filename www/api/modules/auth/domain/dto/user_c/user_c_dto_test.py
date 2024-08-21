import pytest
from unittest.mock import Mock

from ...entity import UserType
from .user_c_dto import UserCDTO


@pytest.mark.parametrize('user, user_credentials, expected', [
    (
        Mock(
            id=1,
            type=UserType.ADMIN,
            given_name='John',
            surname='Doe',
            avatar='avatar.jpg'
        ),
        Mock(
            email='test@test.com',
            sso_provider='google'
        ),
        UserCDTO(
            id=1,
            user_type='ADMIN',
            email='test@test.com',
            given_name='John',
            surname='Doe',
            avatar='avatar.jpg',
            sso_provider='google'
        )
    ),
    (
        Mock(
            id=2,
            type=UserType.STUDENT,
            given_name='Jane',
            surname='Doe',
            avatar='avatar.jpg'
        ),
        Mock(
            email='test@test.com',
            sso_provider=None
        ),
        UserCDTO(
            id=2,
            user_type='STUDENT',
            email='test@test.com',
            given_name='Jane',
            surname='Doe',
            avatar='avatar.jpg'
        )
    )
])
def test_from_uc(user, user_credentials, expected):
    assert UserCDTO.from_uc(user, user_credentials) == expected
