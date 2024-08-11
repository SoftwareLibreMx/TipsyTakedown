from dataclasses import dataclass


@dataclass
class Card:
    id: str
    card_number: str
    security_code: str
    expiration_month: str
    expiration_year: str
    cardholder_name: str
    last_four_digits: str
