from PlayerStatus import PlayerStatus
from PlayerAction import PlayerAction


class Player:

    def __init__(self, name, funds):
        self.name = name
        self.funds = funds
        self.hole_cards = []
        self.status = PlayerStatus.TO_CALL
        self.bet = 0

    def set_hole_cards(self, card1, card2):
        self.hole_cards.append(card1)
        self.hole_cards.append(card2)

    def change_status(self, status):
        self.status = status

    def can_bet(self, bet_value):
        if bet_value > self.funds:
            return False
        else:
            return True

    def make_bet(self, bet_value):
        self.funds = self.funds - bet_value
        self.bet = self.bet + bet_value

    def get_pot(self, pot):
        self.funds += pot