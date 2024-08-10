import pytest
from unittest.mock import patch, Mock

from shared.globals import mercadopago_credentials

from .card_repository import CardRepository, mercadopago


class TestCardRepository:
    @pytest.mark.parametrize('user_email, response, expected_response', [
        ['test@fake_domain.com', [], None],
        [
            'test@fake_domain.com',
            [{'id': 1, 'email': 'test@fake_domain.com'}],
            {'id': 1, 'email': 'test@fake_domain.com'}
        ],
    ])
    @patch.object(mercadopago, 'SDK', Mock())
    def test_get_user_by_email(self, user_email,
                               response, expected_response):
        # Mock
        mock_customer = Mock()
        mock_customer.search.return_value = {
            'response': {
                'results': response
            }
        }

        mock_sdk = Mock()
        mock_sdk.customer.return_value = mock_customer

        mercadopago.SDK.return_value = mock_sdk

        mercadopago_credentials['access_token'] = "something"
        card_repository = CardRepository()

        # Ack
        user = card_repository.get_user_by_email(user_email)

        # Assert
        assert user == expected_response

    @pytest.mark.parametrize('user_email, response, expected_response', [
        [
            'test@fake.domain.com',
            {'id': 1, 'email': 'test@fake_domain.com'},
            {'id': 1, 'email': 'test@fake_domain.com'}
        ],
        [
            'test@fake_domain.com',
            {
                'message': 'invalid parameters ',
                'error': 'bad_request',
                'status': 400,
                'cause': [
                    {
                        'code': '106',
                        'description': 'the email format is invalid'
                    }
                ]
            },
            None
        ],
    ])
    @patch.object(mercadopago, 'SDK', Mock())
    def test_create_user(self, user_email, response, expected_response):
        # mock
        mock_customer = Mock()
        mock_customer.create.return_value = {
            'response': response
        }

        mock_sdk = Mock()
        mock_sdk.customer.return_value = mock_customer

        mercadopago.SDK.return_value = mock_sdk

        mercadopago_credentials['access_token'] = "something"
        card_repository = CardRepository()

        # Ack
        user = card_repository.create_user(user_email)

        # Assert
        assert user == expected_response