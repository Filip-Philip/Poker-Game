from enum import Enum, unique
from functools import total_ordering


@unique
@total_ordering
class Type(Enum):
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value

        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value

        return NotImplemented

    def next(self):
        if self == self.ACE:
            return self.TWO
        return Type(self.value + 1)

    def __str__(self):
        return self.name
