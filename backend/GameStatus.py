from enum import Enum, auto
from functools import total_ordering


@total_ordering
class GameStatus(Enum):
    STARTED = 1

    PREFLOP = 2

    FLOP = 3

    TURN = 4

    RIVER = 5

    SHOWDOWN = 6
    
    ENDED = 7

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value

        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value

        return NotImplemented
