from argparse import Action
from operator import truediv
from pickle import TRUE
from re import S

from numpy import empty
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
        self.deck.fill_deck()
        self.deck.shuffle_deck()
        self.button_player = players[button]
        self.community_cards = []
        self.pot = 0
        self.on_the_table = 0
        self.current_raise = 0
        self.status = GameStatus.STARTED

    def settle_game(self, winner):
        winner.get_pot(self.pot)
        self.pot = 0
        self.status = GameStatus.ENDED

    def add_bets_to_pot(self):
        self.pot += self.on_the_table
        self.on_the_table = 0
        self.players.clear_bets()

    def round_of_betting(self):
        while TRUE:
            for i in range (0, self.players.number_of_players):
                self.print_game_info()
                if self.players.active_players_number == 1:
                    self.add_bets_to_pot()
                    self.settle_game([self.players.current_player])
                    return
                
                if self.players.current_player.status is not PlayerStatus.OUT:
                    actions = self.get_available_actions(self.players.current_player)
                    action = self.get_action(actions)
                    self.handle_action(self.players.current_player, action)
                self.players.next_player()
            
            if self.players.can_end_betting():
                break

        self.add_bets_to_pot()
    
    def get_action(self, actions):
        print(self.players.current_player.name, "turn!")
        print(actions)
        action_number = int(input("Choose one of available actions: "))
        return actions[action_number]

    def print_game_parameters(self):    # For tests
        pass

    def the_pre_flop(self):
        self.status = GameStatus.PREFLOP
        self.on_the_table += Game.big_blind + Game.small_blind
        self.current_raise = Game.big_blind
        self.players.give_hole_cards(self.deck)

        self.players.next_player()
        self.players.current_player.make_bet(Game.small_blind)
        self.players.next_player()
        self.players.current_player.make_bet(Game.big_blind)
        self.players.current_player.change_status(PlayerStatus.IN)
        self.players.next_player()
        
        self.round_of_betting()

    def the_flop(self):
        self.status = GameStatus.FLOP
        self.players.new_turn()
        self.players.change_cur_player(self.button_player)
        self.current_raise = 0
        self.community_cards.append(self.deck.draw_card())
        self.community_cards.append(self.deck.draw_card())
        self.community_cards.append(self.deck.draw_card())
        self.round_of_betting()

    def the_turn(self):
        self.status = GameStatus.TURN
        self.players.new_turn()
        self.players.change_cur_player(self.button_player)
        self.current_raise = 0
        self.community_cards.append(self.deck.draw_card())

        self.round_of_betting()

    def the_river(self):
        self.status = GameStatus.RIVER
        self.players.new_turn()
        self.players.change_cur_player(self.button_player)
        self.current_raise = 0
        self.community_cards.append(self.deck.draw_card())
        self.round_of_betting()

    def showdown(self):
        self.status = GameStatus.SHOWDOWN
        self.players.new_turn()
        active_players = self.players.active_players_list()
        winners = []
        winners.append(active_players[0])
        winner_hand = Hand()
        winner_hand.choose_best(self.community_cards + winners[0].hole_cards)
        hand = Hand()
        print(active_players[0].name, "best hand: ", end="")
        print_hand(winner_hand.cards)

        for i in range(1, len(active_players)):
            hand.choose_best(self.community_cards + active_players[i].hole_cards)
            print(active_players[i].name, "best hand: ", end="")
            print_hand(hand.cards)

            if hand < winner_hand:
                pass
            elif hand == winner_hand:
                winners.append(active_players[i])
            else:
                winners.clear()
                winners.append(active_players[i])
                winner_hand.cards = hand.cards
        
        print("The winner is " + winners[0].name)
        print("Winner's hand: ", end = "")
        print_hand(winner_hand.cards)
        self.settle_game(winners[0])

    def get_available_actions(self, player):
        if player.status == PlayerStatus.OUT:
            return None

        elif player.status == PlayerStatus.TO_CALL:
            if player.can_bet:
                return [PlayerAction.CALL, PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.ALL_IN]
            else:
                return [PlayerAction.FOLD, PlayerAction.ALL_IN]

        elif player.status == PlayerStatus.IN:
                return [PlayerAction.RAISE, PlayerAction.FOLD, PlayerAction.CHECK, PlayerAction.ALL_IN]

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
            self.on_the_table += player.funds
            if to_all > self.current_raise:
                self.current_raise = to_all

        elif action == PlayerAction.RAISE:      # assume default raise_option[0]
            raise_value = Game.raise_options[0]

            if player.can_bet(self.current_raise - player.bet + raise_value):
                player.make_bet(self.current_raise - player.bet + raise_value)
                self.current_raise += raise_value
                self.on_the_table += self.current_raise - player.bet + raise_value
                self.players.after_raise_update(self.current_raise)
                player.change_status(PlayerStatus.IN)
            else:
                self.handle_action(player, PlayerAction.ALL_IN)

    def print_game_info(self):
        print(self.status)
        print("In pot: ", self.pot)
        print("On the table: ", self.on_the_table)
        print("Current raise: ", self.current_raise)
        print_hand(self.community_cards)
        print("Players info:")
        print("name", "status", "bet", sep="   ")
        for player in self.players.players:
            print(player.name, player.status, player.bet, sep="   ")
            print_hand(player.hole_cards)
        print()
    
def print_hand(cards):
    if cards is not empty:
        for card in cards:
            print(card.type, "of", card.suit, end='\t')
        print()