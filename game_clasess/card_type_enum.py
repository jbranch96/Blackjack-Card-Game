from enum import Enum, auto

class CardTypeEnum(Enum):
    ACE = auto() # Making Ace have a default of 1, will handle logic externally for if user wants the value to be 11
    _2 = auto()
    _3 = auto()
    _4 = auto()
    _5 = auto()
    _6 = auto()
    _7 = auto()
    _8 = auto()
    _9 = auto()
    _10 = auto()
    JOKER = 10
    QUEEN = 10
    KING = 10