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
from backend.ActionHandler import ActionHandler


class Game:
    small_blind = 1
    big_blind = 2
    raise_options = [1, 2, 5]

    def __init__(self, players, button):
        self.players = PlayersList(players)
        self.players.optimize_order(button)
        self.deck = Deck()
        self.action_handler = ActionHandler(self)
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
                    actions = self.action_handler.get_available_action(self.players.current_player)
                    action = self.getAction(actions)
                    self.action_handler.handle_action(self.players.current_player, action)
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

        