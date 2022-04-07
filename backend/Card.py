from functools import total_ordering


@total_ordering
class Card:
    def __init__(self, suit, type):
        self.suit = suit
        self.type = type

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.type == other.type

        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.type < other.type

        return NotImplemented

    def __str__(self):
        return self.type.__str__() + " " + self.suit.__str__()



