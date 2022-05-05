"""
from backend.Hand import Hand
from backend.Card import Card
from backend.Suit import Suit
from backend.Type import Type
from backend.Game import Game
from backend.Player import Player

player1 = Player("player1", 100)
player2 = Player("player2", 100)
player3 = Player("player3", 100)

game = Game([player1, player2, player3], 0)
print("Game setup")
game.print_game_info()
game.the_pre_flop()
print("After Pre Flop")
game.print_game_info()
game.the_flop()
print("After Flop")
game.print_game_info()
game.the_turn()
print("After Turn")
game.print_game_info()
game.the_river()
print("After River")
game.print_game_info()
game.showdown()
"""