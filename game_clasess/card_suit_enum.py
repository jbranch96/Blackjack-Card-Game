from enum import Enum, auto

class CardSuitEnum(Enum):
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name.lower() # Sets each value to the lowercase version of the name
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()