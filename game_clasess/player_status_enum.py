from enum import Enum, auto
    
class PlayerStatusEnum(Enum):

        UNDER_21 = auto()
        BLACKJACK = auto()
        BUST = auto()
        STANDING = auto()