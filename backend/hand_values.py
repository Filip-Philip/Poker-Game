from enum import Enum, unique
from functools import total_ordering


@unique
@total_ordering
class HandValues(Enum):
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    PAIR = 2
    HIGH_CARD = 1

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value

        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value

        return NotImplemented

    def __str__(self):
        return self.name


