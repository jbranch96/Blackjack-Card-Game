from random import shuffle

from game_clasess.card_class import Card
from game_clasess.card_type_enum import CardTypeEnum
from game_clasess.card_suit_enum import CardSuitEnum

class Deck:

    def __init__(self):
        self.cards = [
            Card(c_type, c_suit) for c_type in CardTypeEnum.__members__.values() for c_suit in CardSuitEnum.__members__.values()
        ]
        self.shuffle()

    def deal(self) -> Card:
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            raise IndexError("Cannot pop from a deck without any cards.")
    
    def shuffle(self) -> None:
        shuffle(self.cards)