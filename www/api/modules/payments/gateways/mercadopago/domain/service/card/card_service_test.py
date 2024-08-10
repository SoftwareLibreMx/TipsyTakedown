import bcrypt
import unittest
from unittest.mock import Mock

from shared.globals import mercadopago_credentials as mp_credentials
from api.modules.payments.domain.entity import PaymentAudit
from api.modules.payments.domain.dto import Subscription

from ...entity import User
from ...dto import Card
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
        req_card = Card(id='1', last_four_digits='1234',
                        card_token='1234', payment_method_id='visa')
        user = User(id='1', email='test@foo.com', cards=[req_card])
        encrypted_email = self.__encrypt_email(user.email)
        subscription = Subscription(transaction_amount=100.10)
        payment_audit = PaymentAudit(id='1', payment_id='1', user_id='1',
                                     amount=100.10, status='paid')
        payment_response = {'status': 'approved'}

        # Mocks
        mp_repository = Mock()

        mp_repository.get_user_by_email.return_value = {
            'id': user.id,
            'email': user.email,
            'cards': [
                {
                    'id': req_card.id,
                    'last_four_digits': req_card.last_four_digits,
                    'card_token': req_card.card_token,
                    'payment_method_id': req_card.payment_method_id
                }
            ]
        }
        mp_repository.pay_subscription.return_value = payment_response

        payment_audit_repo = Mock()
        payment_audit_repo.create_payment_audit.return_value = payment_audit
        payment_audit_repo.updater_payment_audit.return_value = payment_audit

        mp_card_service = CardService(
            mp_repository, payment_audit_repo)

        # Act
        result = mp_card_service.pay_subscription(
            user, req_card, subscription)

        # Assert
        self.assertEqual(result, payment_response)
        mp_repository.get_user_by_email.assert_called_once_with(
            encrypted_email)
        mp_repository.pay_subscription.assert_called_once_with({
            "transaction_amount": subscription.transaction_amount,
            "token": req_card.card_token,
            "description": "",
            "payment_method_id": req_card.payment_method_id,
            "installments": 1,
            "payer": {
                "email": encrypted_email
            }
        })

        payment_audit_repo.create_payment_audit.assert_called_once_with(
            user.id, req_card.id, subscription)
        payment_audit_repo.update_payment_audit.assert_called_once_with(
            payment_audit.id, payment_response['status'])

    def test_pay_subscription_create_user(self):
        # Setup
        req_card = Card(id='1', last_four_digits='1234',
                        card_token='1234', payment_method_id='visa')
        user = User(id='1', email='test@foo.com', cards=[req_card])
        encrypted_email = self.__encrypt_email(user.email)
        subscription = Subscription(transaction_amount=100.10)
        payment_audit = PaymentAudit(id='1', payment_id='1', user_id='1',
                                     amount=100.10, status='paid')
        payment_response = {'status': 'approved'}

        # Mocks
        mp_repository = Mock()

        mp_repository.get_user_by_email.return_value = None
        mp_repository.create_user.return_value = {
            'id': user.id,
            'email': user.email,
            'cards': [
                {
                    'id': req_card.id,
                    'last_four_digits': req_card.last_four_digits,
                    'card_token': req_card.card_token,
                    'payment_method_id': req_card.payment_method_id
                }
            ]
        }
        mp_repository.pay_subscription.return_value = payment_response

        payment_audit_repo = Mock()
        payment_audit_repo.create_payment_audit.return_value = payment_audit
        payment_audit_repo.updater_payment_audit.return_value = payment_audit

        mp_card_service = CardService(
            mp_repository, payment_audit_repo)

        # Act
        result = mp_card_service.pay_subscription(
            user, req_card, subscription)

        # Assert
        self.assertEqual(result, payment_response)
        mp_repository.get_user_by_email.assert_called_once_with(
            encrypted_email)
        mp_repository.create_user.assert_called_once_with(encrypted_email)
        mp_repository.pay_subscription.assert_called_once_with({
            "transaction_amount": subscription.transaction_amount,
            "token": req_card.card_token,
            "description": "",
            "payment_method_id": req_card.payment_method_id,
            "installments": 1,
            "payer": {
                "email": encrypted_email
            }
        })

        payment_audit_repo.create_payment_audit.assert_called_once_with(
            user.id, req_card.id, subscription)
        payment_audit_repo.update_payment_audit.assert_called_once_with(
            payment_audit.id, payment_response['status'])

    def test_pay_subscription_create_card(self):
        # Setup
        req_card = Card(id='1', last_four_digits='1234',
                        card_token='1234', payment_method_id='visa')
        user = User(id='1', email='test@foo.com', cards=[req_card])
        encrypted_email = self.__encrypt_email(user.email)
        subscription = Subscription(transaction_amount=100.10)
        payment_audit = PaymentAudit(id='1', payment_id='1', user_id='1',
                                     amount=100.10, status='paid')
        payment_response = {'status': 'approved'}

        # Mocks
        mp_repository = Mock()

        mp_repository.get_user_by_email.return_value = {
            'id': user.id,
            'email': user.email,
            'cards': [
                {
                    'id': '2',
                    'last_four_digits': '5678',
                    'card_token': '5678',
                    'payment_method_id': 'mastercard'
                }
            ]
        }
        mp_repository.create_card.return_value = {
            'id': req_card.id,
            'last_four_digits': req_card.last_four_digits,
            'card_token': req_card.card_token,
            'payment_method_id': req_card.payment_method_id
        }
        mp_repository.pay_subscription.return_value = payment_response

        payment_audit_repo = Mock()
        payment_audit_repo.create_payment_audit.return_value = payment_audit
        payment_audit_repo.updater_payment_audit.return_value = payment_audit

        mp_card_service = CardService(
            mp_repository, payment_audit_repo)

        # Act
        result = mp_card_service.pay_subscription(
            user, req_card, subscription)

        # Assert
        self.assertEqual(result, payment_response)
        mp_repository.get_user_by_email.assert_called_once_with(
            encrypted_email)
        mp_repository.create_card.assert_called_once_with(user.id, req_card)
        mp_repository.pay_subscription.assert_called_once_with({
            "transaction_amount": subscription.transaction_amount,
            "token": req_card.card_token,
            "description": "",
            "payment_method_id": req_card.payment_method_id,
            "installments": 1,
            "payer": {
                "email": encrypted_email
            }
        })

        payment_audit_repo.create_payment_audit.assert_called_once_with(
            user.id, req_card.id, subscription)
        payment_audit_repo.update_payment_audit.assert_called_once_with(
            payment_audit.id, payment_response['status'])
