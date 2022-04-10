from PlayerStatus import PlayerStatus
from PlayerAction import PlayerAction


class Player:

    def __init__(self, name, funds):
        self.name = name
        self.funds = funds
        self.hole_cards = []
        self.status = PlayerStatus.IN
        self.bet = 0

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            if len(self.cards) == len(other.cards) == self.FINAL_NUMBER_OF_CARDS:
                return self.hand.is_better_than(other) == 0
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if len(self.cards) == len(other.cards) == self.FINAL_NUMBER_OF_CARDS:
                return self.hand.is_better_than(other) == -1
        return NotImplemented

    def set_hole_cards(self, card1, card2):
        self.hole_cards.append(card1)
        self.hole_cards.append(card2)

    def change_status(self, status):
        self.status = status

    def make_bet(self, bet_value):
        if bet_value > self.funds:
            return False
        else:
            self.funds = self.funds - bet_value
            self.bet = self.bet + bet_value
            return True

    def fold(self):
        self.status = PlayerStatus.OUT

    def give_bet_to_pot(self):
        i = self.bet
        self.bet = 0
        return i

    def get_pot(self, pot):
        self.funds += pot