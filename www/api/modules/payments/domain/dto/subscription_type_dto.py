from dataclasses import dataclass
from typing import Optional


@dataclass
class SubscriptionTypeDTO:
    currency: str
    transaction_amount: float
    id: Optional[str] = None
    payment_cycle: Optional[str] = None
