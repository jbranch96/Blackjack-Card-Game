from dataclasses import dataclass

from game_clasess.card_type_enum import CardTypeEnum
from game_clasess.card_suit_enum import CardSuitEnum

@dataclass
class Card:
    
    type  : CardTypeEnum # Type also contains card value as enum value
    suit  : CardSuitEnum

    def __post_init__(self):
        if self.type.value < 1:
            raise ValueError("Card value cannot be less than 1.")
        if self.type.value > 11:
            raise ValueError("Card value cannot be greater than 11.")
        if self.suit not in (CardSuitEnum.__members__.values()):
            raise ValueError("Invalid specification for card suit.")