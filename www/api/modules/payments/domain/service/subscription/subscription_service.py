from datetime import datetime, timedelta
from typing import Optional

from ...dto import SubscriptionTypeDTO
from ...entity import (
    PaymentAuditModel,
    PaymentCycle,
    PaymentMethod,
    PaymentStatus,
    SubscriptionModel,
    SubscriptionTypeModel
)
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
    def pay(
        self,
        user: dict,
        subscription_type_id: str,
        promo_code: Optional[str],
        payment_method: PaymentMethod,
        card: Optional[dict] = None,
    ) -> tuple[Optional[list[str]], dict]:
        subscription_type = self.st_repository.get(
            subscription_type_id)

        if not subscription_type:
            return ['Subscription type not found'], {}

        payment_method_service = self._get_payment_method(payment_method)

        if not payment_method_service:
            return ['Payment method not found'], {}

        subscription_type = SubscriptionTypeDTO(
            id=subscription_type.id,
            transaction_amount=self._calculate_payment_amount(
                subscription_type, promo_code),
            currency=subscription_type.currency,
            payment_cycle=subscription_type.payment_cycle
        )

        errors, payment_audit_log = self._create_audit_log(
            user,
            subscription_type.transaction_amount,
            subscription_type.currency,
            payment_method
        )

        if errors:
            return errors, {}

        error, response = payment_method_service.pay(
            user, subscription_type, payment_audit_log, card)

        if error:
            error['status'] = PaymentStatus.REJECTED.value
            self.payment_audit_repository.update(payment_audit_log.id, error)
            return error, {}

        payment_audit_log = self.payment_audit_repository.update(
            payment_audit_log.id,
            {
                'status': PaymentStatus.APPROVED.value,
            }
        )

        error, subscription = self._create_subscription(
            user, subscription_type, payment_audit_log)

        if error:
            print(error)
            self.payment_audit_repository.update(payment_audit_log.id, {
                'error': error,
            })
            return error, None

        payment_audit_log = self.payment_audit_repository.update(
            payment_audit_log.id,
            {
                'status': PaymentStatus.APPROVED.value,
            }
        )

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
            self.promo_repository.get_by_code(promo_code)
            if promo_code
            else None
        )

        if promo:
            return subscription_type.price - promo.discount

        return subscription_type.price

    def _create_audit_log(
        self,
        user: dict,
        payment_amount: float,
        currency: str,
        payment_method: PaymentMethod
    ) -> tuple[Optional[list[str]], PaymentAuditModel]:
        error, payment_audit = PaymentAuditModel.from_dict({
            'user_id': user.get('id'),
            'payment_amount': payment_amount,
            'currency': currency,
            'transaction_date': datetime.now(),
            'payment_method': payment_method,
        })

        if error:
            return error, None

        try:
            payment_audit = self.payment_audit_repository.create(payment_audit)
        except Exception as e:
            return [str(e)], None

        return None, payment_audit

    def _get_payment_method(self, method: PaymentMethod):
        return {
            PaymentMethod.CREDIT_CARD.value: self.card_service,
            PaymentMethod.DEBIT_CARD.value: self.card_service,
        }.get(method, None)

    def _create_subscription(
        self,
        user: dict,
        subscription_type: SubscriptionTypeModel,
        payment_audit_log: PaymentAuditModel
    ) -> tuple[Optional[list[str]], SubscriptionModel]:
        error, subscription_model = SubscriptionModel.from_dict({
            'user_id': user.get('id'),
            'subscription_type_id': str(subscription_type.id),
            'payment_log_id': str(payment_audit_log.id),
            'start_date': datetime.now(),
            'end_date': datetime.now() + self._get_datetime_interval(
                subscription_type.payment_cycle),
        })

        if error:
            return error, None

        try:
            subscription = self.subscription_repository.create(
                subscription_model)
        except Exception as e:
            return [str(e)], None

        return None, subscription
