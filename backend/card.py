from functools import total_ordering
from backend.suit import Suit
from backend.type import Type
import os


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

    def get_path_to_image(self):
        path = ['images', 'Averses']
        if self.suit == Suit.CLUBS:
            path.append('Clubs')
        elif self.suit == Suit.HEARTS:
            path.append('Hearts')
        elif self.suit == Suit.SPADES:
            path.append('Spades')
        elif self.suit == Suit.DIAMONDS:
            path.append('Diamonds')

        if self.type == Type.TWO:
            path.append('2.png')
        elif self.type == Type.THREE:
            path.append('3.png')
        elif self.type == Type.FOUR:
            path.append('4.png')
        elif self.type == Type.FIVE:
            path.append('5.png')
        elif self.type == Type.SIX:
            path.append('6.png')
        elif self.type == Type.SEVEN:
            path.append('7.png')
        elif self.type == Type.EIGHT:
            path.append('8.png')
        elif self.type == Type.NINE:
            path.append('9.png')
        elif self.type == Type.TEN:
            path.append('10.png')
        elif self.type == Type.JACK:
            path.append('J.png')
        elif self.type == Type.QUEEN:
            path.append('Q.png')
        elif self.type == Type.KING:
            path.append('K.png')
        elif self.type == Type.ACE:
            path.append('A.png')

        return os.path.join(path[0], path[1], path[2], path[3])
