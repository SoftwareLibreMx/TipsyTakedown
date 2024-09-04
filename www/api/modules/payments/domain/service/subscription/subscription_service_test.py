import pytest
from dataclasses import dataclass
from datetime import timedelta
from unittest.mock import Mock

from .subscription_service import SubscriptionService
from ...entity import PaymentCycle, PaymentMethod, PaymentStatus

mock_credit_card_service = Mock()


@dataclass
class FakePay:
    id: str

    def __eq__(self, other):
        return self.id == other.id


@dataclass
class FakePaymentAuditLog:
    id: str

    def __eq__(self, other):
        return self.id == other.id


@dataclass
class FakeSubscription:
    id: str = None
    rejection_reason: str = None

    def __eq__(self, other):
        return self.rejection_reason == other.rejection_reason\
            and self.id == other.id


class TestSubscriptionService:
    @pytest.mark.parametrize(
        'st_resp, payment_method, create_audit_log, pay_resp, create_subscription, expected',
        [
            [None, None, None, None, None,
                (['Subscription type not found'], {})],
            [
                Mock(price=100, currency='MXN'),
                'Invalid Method',
                None,
                None,
                None,
                (['Payment method not found'], {})
            ],
            [
                Mock(price=100.00, currency='MXN'),
                PaymentMethod.CREDIT_CARD.value,
                ({'error': True}, {}),
                None,
                None,
                ({'error': True}, {})
            ],
            [
                Mock(
                    price=100,
                    id='valid',
                    payment_cycle=PaymentCycle.MONTHLY
                ),
                PaymentMethod.CREDIT_CARD.value,
                (None, Mock(id='valid')),
                ({'eror': True}, None),
                None,
                ({'eror': True, 'status': 'REJECTED'}, {})
            ],
            [
                Mock(
                    price=100,
                    id='valid',
                    payment_cycle=PaymentCycle.MONTHLY
                ),
                PaymentMethod.CREDIT_CARD.value,
                (None, Mock(id='valid')),
                (None, Mock()),
                (FakeSubscription(rejection_reason='test'), None),
                (FakeSubscription(rejection_reason='test'), None)
            ],
            [
                Mock(
                    price=100,
                    id='valid',
                    payment_cycle=PaymentCycle.MONTHLY
                ),
                PaymentMethod.CREDIT_CARD.value,
                (None, FakePaymentAuditLog(id='valid')),
                (None, FakePay(id='valid')),
                (None, FakeSubscription(id='valid')),
                (None, {
                    'subscription': FakeSubscription(id='valid'),
                    'payment_audit_log': FakePaymentAuditLog(id='valid'),
                    'payment_response': FakePay(id='valid'),
                })
            ],
        ]
    )
    def test_pay_subscription(
        self,
        st_resp,
        payment_method,
        create_audit_log,
        pay_resp,
        create_subscription,
        expected
    ):
        subscription_service = SubscriptionService(
            payment_audit_repository=Mock(),
            subscription_type_repository=Mock(),
            subscription_repository=Mock(),
            promo_repository=Mock(),
            card_service=mock_credit_card_service,
        )

        subscription_service.st_repository.get.return_value = st_resp
        subscription_service._create_audit_log = Mock(
            return_value=create_audit_log)

        for i in (create_audit_log or []):
            subscription_service.payment_audit_repository.update.return_value = i

        mock_credit_card_service.pay.return_value = pay_resp
        subscription_service._create_subscription = Mock(
            return_value=create_subscription)

        response = subscription_service.pay(
            user={'id': 'valid'},
            subscription_type_id='valid',
            promo_code=None,
            payment_method=payment_method,
        )

        assert response == expected

    @pytest.mark.parametrize('method, expected', [
        [PaymentMethod.CREDIT_CARD.value, mock_credit_card_service],
        [PaymentMethod.DEBIT_CARD.value, mock_credit_card_service],
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
        [PaymentCycle.MONTHLY.value, timedelta(days=30)],
        [PaymentCycle.ANNUALLY.value, timedelta(days=365)],
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
