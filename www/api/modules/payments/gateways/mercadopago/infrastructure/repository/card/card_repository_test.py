import pytest
from unittest.mock import patch, Mock

from shared.globals import mercadopago_credentials

from .card_repository import CardRepository, mercadopago


class TestCardRepository:
    def test_missing_access_token(self):
        mercadopago_credentials['access_token'] = None
        with pytest.raises(Exception):
            CardRepository()

    @pytest.mark.parametrize(
        'card, token_resp, expected_response',
        [
            [
                Mock(
                    id=1,
                    card_number='5474925432670366',
                    cvv='123',
                    expiration_date='11/25',
                ),
                {
                    'message': 'invalid card_number',
                    'status': 400,
                    'error': 'bad_request',
                    'cause': [
                        {'description': 'invalid card_number', 'code': 'E202'}]
                },
                (
                    {
                        'message': 'invalid card_number',
                        'status': 400,
                        'error': 'bad_request',
                        'cause': [
                            {
                                'description': 'invalid card_number',
                                'code': 'E202'
                            }
                        ]
                    },
                    None
                )
            ],
            [
                Mock(
                    id=1,
                    card_number='5474925432670366',
                    cvv='123',
                    expiration_date='11/25',
                ),
                {
                    'id': '557304207b529e7e79426ce92d14953e',
                    'first_six_digits': '547492',
                    'expiration_month': 11,
                    'expiration_year': 2025,
                    'last_four_digits': '0366',
                    'cardholder': {'identification': {}, 'name': 'APRO'},
                    'status': 'active',
                    'date_created': '2024-08-10T22:43:05.567-04:00',
                    'date_last_updated': '2024-08-10T22:43:05.567-04:00',
                    'date_due': '2024-08-18T22:43:05.567-04:00',
                    'luhn_validation': True,
                    'live_mode': False,
                    'require_esc': False,
                    'card_number_length': 16,
                    'security_code_length': 3
                },
                (None, {
                    'id': '557304207b529e7e79426ce92d14953e',
                    'first_six_digits': '547492',
                    'expiration_month': 11,
                    'expiration_year': 2025,
                    'last_four_digits': '0366',
                    'cardholder': {'identification': {}, 'name': 'APRO'},
                    'status': 'active',
                    'date_created': '2024-08-10T22:43:05.567-04:00',
                    'date_last_updated': '2024-08-10T22:43:05.567-04:00',
                    'date_due': '2024-08-18T22:43:05.567-04:00',
                    'luhn_validation': True,
                    'live_mode': False,
                    'require_esc': False,
                    'card_number_length': 16,
                    'security_code_length': 3
                }),
            ]
        ]
    )
    @patch.object(mercadopago, 'SDK', Mock())
    def test_create_card_token(self, card, token_resp, expected_response):
        # Mock
        mock_card_token = Mock()
        mock_card_token.create.return_value = {
            'response': token_resp
        }

        mock_sdk = Mock()
        mock_sdk.card_token.return_value = mock_card_token

        mercadopago.SDK.return_value = mock_sdk

        mercadopago_credentials['access_token'] = "something"
        card_repository = CardRepository()

        # Ack
        card = card_repository.create_card_token(card)

        # Assert
        assert card == expected_response

    @pytest.mark.parametrize('data, response, expected_response', [
        [
            {
                'token': '557304207b529e7e79426ce92d14953e',
                'transaction_amount': 100,
                'description': 'Title',
                'installments': 1,
                'payment_method_id': 'visa',
                'payer': {
                    'email': 'test@fake_domain.com'
                }
            },
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
            (
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
            )
        ],
        [
            {
                'token': '557304207b529e7e79426ce92d14953e',
                'transaction_amount': 100,
                'description': 'Title',
                'installments': 1,
                'payment_method_id': 'visa',
                'payer': {
                    'email': 'test@fake_domain.com'
                }
            },
            {
                'id': 1,
                'status': 'approved',
                'status_detail': 'accredited',
                'payment_type': 'credit_card',
                'operation_type': 'regular_payment',
                'payer': {
                    'email': 'test@fake_domain.com'
                }
            },
            (
                None,
                {
                    'id': 1,
                    'status': 'approved',
                    'status_detail': 'accredited',
                    'payment_type': 'credit_card',
                    'operation_type': 'regular_payment',
                    'payer': {
                        'email': 'test@fake_domain.com'
                    }
                }
            )
        ],
    ])
    @patch.object(mercadopago, 'SDK', Mock())
    def test_pay_subscription(self, data, response, expected_response):
        # Mock
        mock_payment = Mock()
        mock_payment.create.return_value = {
            'response': response
        }

        mock_sdk = Mock()
        mock_sdk.payment.return_value = mock_payment

        mercadopago.SDK.return_value = mock_sdk

        mercadopago_credentials['access_token'] = "something"
        card_repository = CardRepository()

        # Ack
        payment = card_repository.pay_subscription(data)

        # Assert
        assert payment == expected_response
