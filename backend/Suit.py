from enum import Enum, unique, auto


@unique
class Suit(Enum):
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()

    def __str__(self):
        return self.name
