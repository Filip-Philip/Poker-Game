from backend.player_status import PlayerStatus
from backend.player_action import PlayerAction


def get_available_actions(player):
    if player.status == PlayerStatus.TO_MOVE:
        return [PlayerAction.RAISE, PlayerAction.CHECK, PlayerAction.FOLD, PlayerAction.ALL_IN]

    if player.status == PlayerStatus.OUT:
        return []

    elif player.status == PlayerStatus.TO_CALL:
        return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.ALL_IN]

    elif player.status == PlayerStatus.IN:
        return [PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.CHECK, PlayerAction.ALL_IN]

    elif player.status == PlayerStatus.CHECKED:
        return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.ALL_IN]

    elif player.status == PlayerStatus.ALL_IN:
        return []


class Player:
    STARTING_FUNDS = 100

    def __init__(self, name, funds):
        self.name = name
        self.funds = funds
        self.hole_cards = []
        self.status = PlayerStatus.TO_MOVE
        self.bet = 0

    def set_hole_cards(self, card1, card2):
        self.hole_cards.clear()
        self.hole_cards.append(card1)
        self.hole_cards.append(card2)

    def change_status(self, status):
        self.status = status

    def can_bet(self, bet_value):
        if bet_value >= self.funds:
            return False
        else:
            return True

    def make_bet(self, bet_value):
        self.funds = self.funds - bet_value
        self.bet = self.bet + bet_value

    def get_pot(self, pot):
        self.funds += pot

    def get_info(self):
        return self.name, str(self.funds) + " - " + str(self.bet), self.status.name
