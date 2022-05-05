from GUI.gui import Gui
from backend.Game import Game
from backend.Player import Player
from backend.Card import Card
from backend.Type import Type
from backend.Suit import Suit

WIDTH, HEIGHT = 1500, 800
player1 = Player("player1", 100)
player2 = Player("player2", 100)
player3 = Player("player3", 100)
player4 = Player("player4", 100)
player5 = Player("player5", 100)
player6 = Player("player6", 100)
#

game = Game([player1, player2, player3, player4, player5, player6], 0)
gui = Gui(WIDTH, HEIGHT, game)
gui.run()
