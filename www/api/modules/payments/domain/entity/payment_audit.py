from dataclasses import dataclass


@dataclass
class PaymentAudit:
    id: str
    payment_id: str
    user_id: str
    amount: float
    status: str
