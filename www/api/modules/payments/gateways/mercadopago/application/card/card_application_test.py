import pytest
from unittest.mock import patch, Mock

from . import card_application

mock_card_repository = Mock()
mock_user_service = Mock()
mock_card_service = Mock()


@patch.object(card_application, 'CardRepository', mock_card_repository)
@patch.object(card_application, 'UserService', mock_user_service)
@patch.object(card_application, 'CardService',
              Mock(return_value=mock_card_service))
def test_init():
    card_application.pay({
        'id': 'test',
        'name': 'John Doe',
        'email': 'test'
    }, 1, Mock())

    mock_card_repository.assert_called_once()
    mock_user_service.assert_called_once()
    mock_card_service.pay.assert_called_once()


@patch.object(card_application, 'CardRepository', mock_card_repository)
@patch.object(card_application, 'UserService', mock_user_service)
@patch.object(card_application, 'CardService',
              Mock(return_value=mock_card_service))
def test_wrong_user():
    errors, _ = card_application.pay({
        'id': 'test',
        'name': 'John Doe',
    }, 1, 1)

    assert errors == ['email is required']
