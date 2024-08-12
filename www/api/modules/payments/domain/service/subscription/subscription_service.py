from datetime import datetime, timedelta
from typing import Optional

from ...entity import PaymentCycle, PaymentMethod, PaymentStatus
from ..card.card_service import CardService
from ....infraestructure.repository import (
    PaymentAuditRepository, PromoRepository,
    SubscriptionRepository, SubscriptionTypeRepository
)


class SubscriptionService:
    def __init__(
        self,
        card_service: CardService,
        payment_audit_repository: PaymentAuditRepository,
        promo_repository: PromoRepository,
        subscription_repository: SubscriptionRepository,
        subscription_type_repository: SubscriptionTypeRepository,
    ) -> None:
        # Payment Methods
        self.card_service = card_service

        # Repositories
        self.payment_audit_repository = payment_audit_repository
        self.promo_repository = promo_repository
        self.subscription_repository = subscription_repository
        self.st_repository = subscription_type_repository

    # TODO: this only takes into consideration new subscriptions
    def pay_subscription(
        self,
        user: dict,
        subscription_type_id: str,
        promo_code: Optional[str],
        payment_method: PaymentMethod,
        card: Optional[dict] = None,
    ) -> tuple[Optional[list[str]], dict]:
        subscription_type = self.st_repository.get_subscription(
            subscription_type_id)

        if not subscription_type:
            return ['Subscription type not found'], {}

        payment_amount = self._calculate_payment_amount(
            subscription_type, promo_code)

        payment_method_service = self._get_payment_method(payment_method)

        if not payment_method_service:
            return ['Payment method not found'], {}

        payment_audit_log = self.payment_audit_repository.create({
            'user_id': user['id'],
            'payment_amount': payment_amount,
            'currency': subscription_type.currency,
            'transaction_date': datetime.now(),
            'payment_method': payment_method,
        })

        error, response = payment_method_service.pay(
            user, payment_amount, payment_audit_log, card)

        if error:
            self.payment_audit_repository.update(payment_audit_log.id, {
                'status': PaymentStatus.REJECTED.value,
                'error': error,
                'rejection_reason': error.rejection_reason
            })
            return error, {}

        subscription = self.subscription_repository.create({
            'user_id': user['id'],
            'subscription_type_id': subscription_type.id,
            'payment_audit_id': payment_audit_log.id,
            'start_date': datetime.now(),
            'end_date': datetime.now() + self._get_datetime_interval(
                subscription_type.payment_cycle),
        })

        self.payment_audit_repository.update(payment_audit_log.id, {
            'status': PaymentStatus.APPROVED.value,
        })

        return None, {
            'subscription': subscription,
            'payment_audit_log': payment_audit_log,
            'payment_response': response,
        }

    def _get_datetime_interval(self, payment_cycle: PaymentCycle):
        return {
            PaymentCycle.MONTHLY: timedelta(days=30),
            PaymentCycle.ANNUALLY: timedelta(days=365),
        }.get(payment_cycle, timedelta(days=0))

    def _calculate_payment_amount(self, subscription_type, promo_code):
        promo = (
            self.promo_repository.get_promo(promo_code)
            if promo_code
            else None
        )

        if promo:
            return subscription_type.price - promo.discount

        return subscription_type.price

    def _get_payment_method(self, method: PaymentMethod):
        return {
            PaymentMethod.CREDIT_CARD: self.card_service,
            PaymentMethod.DEBIT_CARD: self.card_service,
        }.get(method, None)
