import pytest
from dataclasses import dataclass
from datetime import timedelta
from unittest.mock import Mock

from .subscription_service import SubscriptionService
from ...entity import PaymentCycle, PaymentMethod

mock_credit_card_service = Mock()


@dataclass
class FakePayError:
    rejection_reason: str

    def __eq__(self, other):
        return self.rejection_reason == other.rejection_reason


@dataclass
class FakePaymentAuditLog:
    id: str

    def __eq__(self, other):
        return self.id == other.id


class TestSubscriptionService:
    @pytest.mark.parametrize('st_resp, payment_method, pay_resp, paudit_resp, expected', [
        [None, None, None, None, (['Subscription type not found'], {})],
        [Mock(price=100, currency='MXN'), 'Invalid Method',
         None, None, (['Payment method not found'], {})],
        [
            Mock(price=100),
            PaymentMethod.CREDIT_CARD,
            (FakePayError(rejection_reason='Not pass'), {}),
            Mock(id='valid'),
            (FakePayError(rejection_reason='Not pass'), {})
        ],
        [
            Mock(price=100, id='valid', payment_cycle=PaymentCycle.MONTHLY),
            PaymentMethod.CREDIT_CARD,
            (None, {}),
            FakePaymentAuditLog('valid'),
            (None, {
                'subscription': 'subscription',
                'payment_audit_log': FakePaymentAuditLog('valid'),
                'payment_response': {}
            })
        ],
    ])
    def test_pay_subscription(
            self, st_resp, payment_method, pay_resp, paudit_resp, expected):
        subscription_service = SubscriptionService(
            payment_audit_repository=Mock(),
            subscription_type_repository=Mock(),
            subscription_repository=Mock(),
            promo_repository=Mock(),
            card_service=mock_credit_card_service,
        )

        subscription_service.st_repository.get.return_value = st_resp
        mock_credit_card_service.pay.return_value = pay_resp
        subscription_service.payment_audit_repository.create.return_value = paudit_resp
        subscription_service.subscription_repository.create.return_value = 'subscription'

        response = subscription_service.pay_subscription(
            user={'id': 'valid'},
            subscription_type_id='valid',
            promo_code=None,
            payment_method=payment_method,
        )

        assert response == expected

    @pytest.mark.parametrize('method, expected', [
        [PaymentMethod.CREDIT_CARD, mock_credit_card_service],
        [PaymentMethod.DEBIT_CARD, mock_credit_card_service],
        ['invalid', None],
    ])
    def test__get_payment_method(self, method, expected):
        subscription_service = SubscriptionService(
            payment_audit_repository=Mock(),
            subscription_type_repository=Mock(),
            subscription_repository=Mock(),
            promo_repository=Mock(),
            card_service=mock_credit_card_service,
        )

        assert subscription_service._get_payment_method(method) == expected

    @pytest.mark.parametrize('payment_cycle, expected', [
        [PaymentCycle.MONTHLY, timedelta(days=30)],
        [PaymentCycle.ANNUALLY, timedelta(days=365)],
        ['invalid', timedelta(days=0)],
    ])
    def test__get_datetime_interval(self, payment_cycle, expected):
        subscription_service = SubscriptionService(
            payment_audit_repository=Mock(),
            subscription_type_repository=Mock(),
            subscription_repository=Mock(),
            promo_repository=Mock(),
            card_service=mock_credit_card_service,
        )

        assert subscription_service._get_datetime_interval(
            payment_cycle) == expected

    @pytest.mark.parametrize('price, promo_code, discound, expected', [
        [100.00, 'valid', 10.10, 89.90],
        [100, None, 0, 100],
    ])
    def test__calculate_payment_amount(
            self, price, promo_code, discound, expected):
        subscription_service = SubscriptionService(
            payment_audit_repository=Mock(),
            subscription_type_repository=Mock(),
            subscription_repository=Mock(),
            promo_repository=Mock(),
            card_service=mock_credit_card_service,
        )

        subscription_type = Mock(price=price)
        promo = Mock(discount=discound)
        subscription_service.promo_repository.get_by_code.return_value = promo

        assert subscription_service._calculate_payment_amount(
            subscription_type, promo_code) == expected
