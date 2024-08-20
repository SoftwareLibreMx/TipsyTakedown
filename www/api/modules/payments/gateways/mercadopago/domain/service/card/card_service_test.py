import bcrypt
import pytest
from unittest.mock import Mock

from shared.globals import mercadopago_credentials as mp_credentials
from api.modules.payments.domain.entity import RejectionReason

from .card_service import CardService


class TestCardService:
    def __encrypt_email(self, email):
        fake_domain = mp_credentials['fake_domain']
        salt = mp_credentials['hidde_user_email_salt']
        encrypted_email = bcrypt.hashpw(
            email.encode('utf-8'), salt).decode('utf-8')
        return f'{encrypted_email}@{fake_domain}'

    def card_service_factory(self):
        mp_card_repository = Mock()

        return (
            CardService(
                Mock(),
                mp_card_repository
            ),
            mp_card_repository
        )

    @pytest.mark.parametrize(
        'mock_card, mock_card_token_resp, pay_subs_resp, expected_response',
        [
            (
                Mock(card_number='123'), None,
                None, (['Card number not valid'], None)
            ),
            (
                Mock(card_number='423'),
                ({'something': True}, None),
                None,
                ({
                    'error': 'Status None error []',
                    'rejection_reason': RejectionReason.UNKNOWN.value
                }, None)
            ),
            (
                Mock(card_number='423'),
                (None, {'id': '123'}),
                ({'something': True}, None),
                ({
                    'error': 'Status None error []',
                    'rejection_reason': RejectionReason.UNKNOWN.value
                }, None)
            ),
            (
                Mock(card_number='423'),
                (None, {'id': '123'}),
                (None, {'something': True}),
                ([], {'something': True})
            )
        ]
    )
    def test_pay(
        self,
        mock_card,
        mock_card_token_resp,
        pay_subs_resp,
        expected_response
    ):
        card_service, mpc_repository = self.card_service_factory()

        mpc_repository.create_card_token.return_value = mock_card_token_resp
        mpc_repository.pay_subscription.return_value = pay_subs_resp

        resp = card_service.pay(Mock(), mock_card, 100)

        assert resp == expected_response
