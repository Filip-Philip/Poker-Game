from PlayerStatus import PlayerStatus
from PlayerAction import PlayerAction
from Deck import Deck
from Player import Player

class PlayersList:

    def __init__(self, players):
        self.players = players
        self.number_of_players = len(players)
        self.current_player = None

    def change_cur_player(self, player):
        self.current_player = self.players[self.players.index(player)]


    def add_player(self, player):
        self.players.append(player)
        self.number_of_players += 1

    def optimize_order(self, button):
        game_order = [0] * self.number_of_players
        i = button
        j = 0

        while j < self.number_of_players:
            game_order[j] = i % self.number_of_players
            j += 1
            i += 1

        self.players = [self.players[i] for i in game_order]
        self.change_cur_player(self.players[0])

    def next_player(self):
        self.current_player = self.players[(self.players.index(self.current_player) + 1) % self.number_of_players]

    def active_players_number(self):
        i = 0
        for player in self.players:
             if player.status != PlayerStatus.OUT:
                i += 1

        return i

    def active_players_list(self):
        active_players = []
        for player in self.players:
             if player.status == PlayerStatus.IN:
                active_players.append(player)

        return active_players

    def reset_players_statuses(self):
        for player in self.players:
            player.change_status(PlayerStatus.IN)

    def can_end_betting(self):
        for player in self.players:
            if player.status not in [PlayerStatus.IN, PlayerStatus.CHECKED, PlayerStatus.OUT, PlayerStatus.ALL_IN]:
                return False

        return True

    def give_hole_cards(self, deck):
        for player in self.players:
            player.set_hole_cards(deck.draw_card(), deck.draw_card())

    def clear_bets(self):
        for player in self.players:
            player.bet = 0

    def new_turn(self):
        for player in self.players:
            if player.status not in [PlayerStatus.OUT, PlayerStatus.ALL_IN]:
                player.change_status(PlayerStatus.IN)

    def after_raise_update(self, current_raise):
        for player in self.players:
            if player.bet != current_raise and player.status in [PlayerStatus.TO_CALL, PlayerStatus.CHECKED, PlayerStatus.IN]:
                player.change_status(PlayerStatus.TO_CALL)