from backend.type import Type
from backend.suit import Suit
from backend.card import Card
from random import shuffle


class Deck:
    def __init__(self):
        self.cards = []

    def fill_deck(self):
        for _, type in Type.__members__.items():
            for _, suit in Suit.__members__.items():
                card = Card(suit, type)
                self.cards.append(card)

    def shuffle_deck(self):
        shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()
