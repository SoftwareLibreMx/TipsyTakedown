import bcrypt
import unittest
from unittest.mock import Mock

from shared.globals import mercadopago_credentials as mp_credentials
from api.modules.payments.domain.entity import Card, PaymentAudit
from api.modules.payments.domain.dto import Subscription

from ...entity import User
from .card_service import CardService


class CardServiceTest(unittest.TestCase):
    def __encrypt_email(self, email):
        fake_domain = mp_credentials['fake_domain']
        salt = mp_credentials['hidde_user_email_salt']
        encrypted_email = bcrypt.hashpw(
            email.encode('utf-8'), salt).decode('utf-8')
        return f'{encrypted_email}@{fake_domain}'

    def test_pay_subscription(self):
        # Setup
        req_card = Card(
            id=1,
            card_number='5474925432670366',
            security_code='123',
            expiration_month=11,
            expiration_year=2025,
            cardholder_name='APRO',
            last_four_digits='0366'
        )
        user = User(id='1', email='test@foo.com')
        encrypted_email = self.__encrypt_email(user.email)
        subscription = Subscription(transaction_amount=100.10)
        payment_audit = PaymentAudit(
            id='1',
            payment_id='1',
            user_id='1',
            amount=100.10,
            status='paid'
        )
        payment_response = {'status': 'approved'}
        card_token = {
            'id': '1234',
            'last_four_digits': req_card.card_number[-4:]
        }
        payment_method_id = 'master'

        # Mocks
        mp_repository = Mock()

        mp_repository.get_user_by_email.return_value = {
            'id': user.id,
            'email': user.email,
        }
        mp_repository.create_card_token.return_value = card_token
        mp_repository.pay_subscription.return_value = payment_response

        payment_audit_repo = Mock()
        payment_audit_repo.create_payment_audit.return_value = payment_audit
        payment_audit_repo.updater_payment_audit.return_value = payment_audit

        mp_card_service = CardService(mp_repository, payment_audit_repo)

        # Act
        result = mp_card_service.pay_subscription(user, req_card, subscription)

        # Assert
        self.assertEqual(result, (None, payment_response))
        mp_repository.pay_subscription.assert_called_once_with({
            "transaction_amount": subscription.transaction_amount,
            "token": card_token['id'],
            "description": "",
            "payment_method_id": payment_method_id,
            "installments": 1,
            "payer": {
                "email": encrypted_email
            }
        })
        mp_repository.create_card_token.assert_called_once_with(req_card)

        payment_audit_repo.create_payment_audit.assert_called_once_with(
            user.id, req_card.card_number[-4:], subscription)
        payment_audit_repo.update_payment_audit.assert_called_once_with(
            payment_audit.id, payment_response['status'])

    def test_pay_subscription_payment_method_not_valid(self):
        # Setup
        req_card = Card(
            id=1,
            card_number='3474925432670366',
            security_code='123',
            expiration_month=11,
            expiration_year=2025,
            cardholder_name='APRO',
            last_four_digits='0366'
        )
        user = User(id='1', email='test@domain.fake.com')
        subscription = Subscription(transaction_amount=100.10)

        # Mocks
        mp_repository = Mock()
        payment_audit_repo = Mock()
        mp_card_service = CardService(
            mp_repository, payment_audit_repo)

        # Act
        result = mp_card_service.pay_subscription(user, req_card, subscription)

        # Assert
        self.assertEqual(result, (['Card number not valid'], None))
        mp_repository.get_user_by_email.assert_not_called()
        mp_repository.create_user.assert_not_called()
        mp_repository.pay_subscription.assert_not_called()
        mp_repository.create_card_token.assert_not_called()
        payment_audit_repo.create_payment_audit.assert_not_called()
        payment_audit_repo.update_payment_audit.assert_not_called()

    def test_pay_subscription_invalid_card_token(self):
        # Setup
        req_card = Card(
            id=1,
            card_number='5474 9254 3267 0366',
            security_code='123',
            expiration_month=11,
            expiration_year=2025,
            cardholder_name='APRO',
            last_four_digits='0366'
        )
        user = User(id='1', email='test@domain.fake.com')
        encrypted_email = self.__encrypt_email(user.email)
        subscription = Subscription(transaction_amount=100.10)
        payment_audit = PaymentAudit(
            id='1',
            payment_id='1',
            user_id='1',
            amount=100.10,
            status='paid'
        )
        payment_response = {'status': 'approved'}
        card_token = None

        # Mocks
        mp_repository = Mock()

        mp_repository.get_user_by_email.return_value = {
            'id': user.id,
            'email': user.email,
        }
        mp_repository.create_card_token.return_value = card_token
        mp_repository.pay_subscription.return_value = payment_response

        payment_audit_repo = Mock()
        payment_audit_repo.create_payment_audit.return_value = payment_audit
        payment_audit_repo.updater_payment_audit.return_value = payment_audit

        mp_card_service = CardService(
            mp_repository, payment_audit_repo)

        # Act
        result = mp_card_service.pay_subscription(user, req_card, subscription)

        # Assert
        self.assertEqual(result, (['Error processing card'], None))
        mp_repository.pay_subscription.assert_not_called()
        mp_repository.create_card_token.assert_called_once_with(req_card)
        payment_audit_repo.create_payment_audit.assert_not_called()
        payment_audit_repo.update_payment_audit.assert_not_called()
