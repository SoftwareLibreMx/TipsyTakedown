from enum import Enum


class PaymentMethod(Enum):
    CREDIT_CARD = 'CREDIT_CARD'
    DEBIT_CARD = 'DEBIT_CARD'
    MERCADO_PAGO = 'MERCADO_PAGO'
    CASH = 'CASH'
    ATM = 'ATM'
    SPEI_TRANSFER = 'SPEI_TRANSFER'
