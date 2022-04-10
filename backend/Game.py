from argparse import Action
from re import S
from Deck import Deck
from Hand import Hand
from Card import Card
from Player import Player
from PlayerStatus import PlayerStatus
from PlayerAction import PlayerAction
from PlayersList import PlayersList
from GameStatus import GameStatus


class Game:
    small_blind = 1
    big_blind = 2
    raise_options = [1, 2, 5]

    def __init__(self, players, button):
        self.players = PlayersList(players)
        self.players.optimize_order(button)
        self.deck = Deck()
        self.button_player = players[button]
        self.community_cards = []
        self.pot = 0
        self.on_the_table = 0
        self.current_raise = 0
        self.status = GameStatus.PENDING

    def settle_game(self, winners):
        for i in len(winners):
            winners.get_pot(self.pot / len(winners))
        self.pot = 0
        self.status = GameStatus.ENDED

    def add_bets_to_pot(self):
        self.pot += self.on_the_table
        self.on_the_table = 0

    def round_of_betting(self):
        while not self.players.can_end_betting():
            for i in range (0, self.players.number_of_players):
                if self.players.active_players_number == 1:
                    self.add_bets_to_pot()
                    self.settle_game([self.players.current_player])
                    return
                
                if self.players.current_player.status is not PlayerStatus.OUT:
                    actions = self.get_available_actions(self.players.current_player)
                    action = self.getAction(actions)
                    self.handle_action(self.players.current_player, action)
                self.players.next_player()
            
            if self.players.all_checked:
                break

        self.add_bets_to_pot()
    
    def get_action(self, actions):   # For tests. Possibly for future
        return actions[0]

    def print_game_parameters(self):    # For tests
        pass

    def the_pre_flop(self):
        self.current_raise = Game.big_blind
        self.players.give_hole_cards(self.deck)

        self.players.next_player()
        self.players.current_player.make_bet(Game.small_blind)
        self.players.next_player()
        self.players.current_player.make_bet(Game.small_blind)
        self.players.next_player()
        
        self.round_of_betting()

    def the_flop(self):
        self.players.change_cur_player(self.button_player)
        self.current_raise = 0
        self.community_cards.draw(self.deck.draw_card)
        self.community_cards.draw(self.deck.draw_card)
        self.community_cards.draw(self.deck.draw_card)
        self.round_of_betting()

    def the_turn(self):
        self.players.change_cur_player(self.button_player)
        self.current_raise = 0
        self.community_cards.append(self.deck.draw_card)

        self.round_of_betting()

    def the_river(self):
        self.players.change_cur_player(self.button_player)
        self.current_raise = 0
        self.community_cards.draw(self.deck.draw_card)
        self.round_of_betting()

    def showdown(self):
        active_players = self.players.active_players_list()
        winners = [active_players[0]]
        winner_hand = Hand().choose_best(self.community_cards + winners[0].hole_cards)

        for i in range(1, active_players.number_of_players):
            hand = Hand().choose_best(self.community_cards + active_players[i].hole_cards)
            if hand < winner_hand:
                pass
            elif hand == winner_hand:
                winners.append(active_players[i])
            else:
                winners = []
                winners.append(active_players[i])
                winner_hand = hand
        
        self.settle_game(winners)

    def get_available_actions(self, player):
        if player.status == PlayerStatus.OUT:
            return None

        elif player.status == PlayerStatus.TO_CALL:
            if player.can_bet:
                return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.ALL_IN]
            else:
                return [PlayerAction.FOLD, PlayerAction.ALL_IN]

        elif player.status == PlayerStatus.IN:
            if self.current_raise > 0:
                return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.ALL_IN]
            else:
                return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.CHECK, PlayerAction.ALL_IN]

        elif player.status == PlayerStatus.CHECKED:
            return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.ALL_IN]
            
        elif player.status == PlayerStatus.ALL_IN:
            return [PlayerAction.CHECK]

    def handle_action(self, player, action):
        if action == PlayerAction.CALL:
            to_call = self.current_raise - player.bet
            player.make_bet(to_call)
            self.on_the_table += to_call
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
                self.players.after_raise_update(self.current_raise)
            else:
                self.handle_action(player, PlayerAction.ALL_IN)

