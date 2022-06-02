from argparse import Action
from operator import truediv
from pickle import TRUE
from re import S

from backend.Deck import Deck
from backend.Hand import Hand
from backend.Card import Card
from backend.Player import Player
from backend.PlayerStatus import PlayerStatus
from backend.PlayerAction import PlayerAction
from backend.PlayersList import PlayersList
from backend.GameStatus import GameStatus
from backend.Player import get_available_actions


class Game:
    small_blind = 1
    big_blind = 2
    raise_options = [1, 2, 5]

    def __init__(self, players, button):
        self.players = PlayersList(players)
        self.players.optimize_order(button)
        self.deck = Deck()
        self.deck.fill_deck()
        self.deck.shuffle_deck()
        self.button = button
        self.button_player = players[button]
        self.community_cards = []
        self.pot = 0
        self.on_the_table = 0
        self.current_raise = 0
        self.status = GameStatus.STARTED
        self.winners = None

    def settle_game(self):
        self.add_bets_to_pot()
        if self.players.active_players_number() == 1:
            winner = self.players.get_last_player()
            winner.get_pot(self.pot)
        else:
            reward = self.pot // len(self.winners)
            for winner in self.winners:
                winner.get_pot(reward)

        self.pot = 0
        self.status = GameStatus.ENDED

    def add_bets_to_pot(self):
        self.pot += self.on_the_table
        self.on_the_table = 0
        self.players.clear_bets()

    def change_game_status(self):
        self.status = self.status.next()
        self.add_bets_to_pot()
        if self.status == GameStatus.PREFLOP:
            self.the_pre_flop()
        if self.status == GameStatus.FLOP:
            self.the_flop()
        if self.status == GameStatus.TURN:
            self.the_turn()
        if self.status == GameStatus.RIVER:
            self.the_river()
        if self.status == GameStatus.SHOWDOWN:
            self.showdown()
        if self.status == GameStatus.ENDED:
            self.settle_game()

    def can_end_betting(self):
        for player in self.players.list:
            if player.status not in [PlayerStatus.IN, PlayerStatus.CHECKED, PlayerStatus.OUT, PlayerStatus.ALL_IN]:
                return False
        return True

    def can_still_play(self):
        if self.players.active_players_number() == 1:
            return False
        return True

    def the_pre_flop(self):
        for player in self.players.list:
            player.change_status(PlayerStatus.TO_CALL)
        self.on_the_table += Game.big_blind + Game.small_blind
        self.current_raise = Game.big_blind

        self.players.give_hole_cards(self.deck)

        self.players.current_player.make_bet(Game.small_blind)

        self.players.next_player()
        self.players.current_player.make_bet(Game.big_blind)
        self.players.current_player.change_status(PlayerStatus.TO_MOVE)

        self.players.next_player()

    def the_flop(self):
        self.players.new_turn()
        self.current_raise = 0
        self.community_cards.append(self.deck.draw_card())
        self.community_cards.append(self.deck.draw_card())
        self.community_cards.append(self.deck.draw_card())

    def the_turn(self):
        self.players.new_turn()
        self.current_raise = 0
        self.community_cards.append(self.deck.draw_card())

    def the_river(self):
        self.players.new_turn()
        self.current_raise = 0
        self.community_cards.append(self.deck.draw_card())

    def showdown(self):
        self.players.new_turn()
        active_players = self.players.active_players_list()
        self.winners = [active_players[0]]
        winner_hand = Hand()
        winner_hand.choose_best(self.community_cards + self.winners[0].hole_cards)
        hand = Hand()

        for i in range(1, len(active_players)):
            hand.choose_best(self.community_cards + active_players[i].hole_cards)

            if hand < winner_hand:
                pass
            elif hand == winner_hand:
                self.winners.append(active_players[i])
            else:
                self.winners.clear()
                self.winners.append(active_players[i])
                winner_hand.cards = hand.cards

    def handle_action(self, player, action):
        if action not in get_available_actions(player):
            return
        if action == PlayerAction.CALL:
            to_call = self.current_raise - player.bet
            player.make_bet(to_call)
            self.on_the_table += to_call
            player.change_status(PlayerStatus.IN)

        elif action == PlayerAction.CHECK:
            player.change_status(PlayerStatus.CHECKED)

        elif action == PlayerAction.FOLD:
            player.change_status(PlayerStatus.OUT)

        elif action == PlayerAction.ALL_IN:
            player.change_status(PlayerStatus.ALL_IN)
            to_all = player.bet + player.funds
            self.on_the_table += player.funds
            player.make_bet(player.funds)
            if to_all > self.current_raise:
                self.current_raise = to_all

        elif action == PlayerAction.RAISE:  # assume default raise_option[0]
            raise_value = Game.raise_options[0]

            if player.can_bet(self.current_raise - player.bet + raise_value):
                self.current_raise += raise_value
                self.on_the_table += self.current_raise - player.bet
                player.make_bet(self.current_raise - player.bet)
                self.players.after_raise_update(self.current_raise)
                player.change_status(PlayerStatus.IN)
            else:
                self.handle_action(player, PlayerAction.ALL_IN)

        self.players.next_player()

    def print_game_info(self):
        print(self.status)
        print("In pot: ", self.pot)
        print("On the table: ", self.on_the_table)
        print("Current raise: ", self.current_raise)
        print("Players info:")
        print("name", "status", "bet", sep="   ")
        for player in self.players.list:
            print(player.name, player.status, player.bet, sep="   ")
        print()
