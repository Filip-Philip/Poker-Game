from PlayerStatus import PlayerStatus
from PlayerAction import PlayerAction
from Player import Player
from Game import Game

class ActionHandler:
    def __init__(self, game):
        self.game = game

    def get_available_action(self, player):
        if player.status == PlayerStatus.OUT:
            return None

        elif player.status == PlayerStatus.TO_CALL:
            if player.can_bet:
                return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.ALL_IN]
            else:
                return [PlayerAction.FOLD, PlayerAction.ALL_IN]

        elif player.status == PlayerStatus.IN:
            if self.game.current_raise > 0:
                return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.ALL_IN]
            else:
                return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.CHECK, PlayerAction.ALL_IN]

        elif player.status == PlayerStatus.CHECKED:
            return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.ALL_IN]
            
        elif player.status == PlayerStatus.ALL_IN:
            return [PlayerAction.CHECK]

    def handle_action(self, player, action):
        if action == PlayerAction.CALL:
            to_call = self.game.current_raise - player.bet
            player.make_bet(to_call)
            self.game.on_the_table += to_call
            player.change_status(PlayerStatus.IN)
        
        elif action == PlayerAction.CHECK and player.status is not PlayerStatus.ALL_IN:
            player.change_status(PlayerStatus.CHECKED)

        elif action == PlayerAction.FOLD:
            player.change_status(PlayerStatus.OUT)

        elif action == PlayerAction.ALL_IN:
            player.change_status(PlayerStatus.ALL_IN)
            to_all = player.bet + player.funds
            player.make_bet(player.funds)
            self.game.on_the_table += player.funds
            if to_all > self.game.current_raise:
                self.game.current_raise = to_all


        elif action == PlayerAction.RAISE:      # assume default raise_option[0]
            raise_value = Game.raise_options[0]

            if player.can_bet(self.game.current_raise - player.bet + raise_value):
                player.make_bet(self.game.current_raise - player.bet + raise_value)
                self.game.current_raise += raise_value
                self.after_raise_update()
            else:
                self.handle_action(player, PlayerAction.ALL_IN)

    def after_raise_update(self):
        for player in self.game.players:
            if player.bet != self.game.current_raise and player.status in [PlayerStatus.TO_CALL, PlayerStatus.CHECKED, PlayerStatus.IN]:
                player.change_status(PlayerStatus.TO_CALL)
            