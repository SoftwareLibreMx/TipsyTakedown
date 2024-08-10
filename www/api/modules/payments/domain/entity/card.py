from dataclasses import dataclass


@dataclass
class Card:
    id: str
    last_four_digits: str
