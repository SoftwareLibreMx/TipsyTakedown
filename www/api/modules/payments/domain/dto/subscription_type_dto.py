from dataclasses import dataclass


@dataclass
class SubscriptionTypeDTO:
    currency: str
    transaction_amount: float
