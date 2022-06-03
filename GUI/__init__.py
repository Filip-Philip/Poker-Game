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

<<<<<<< HEAD
game1 = Game([player1, player2], 0)
game2 = Game([player1, player2, player3, player4, player5, player6], 0)
gui1 = Gui(WIDTH, HEIGHT, game1)
gui2 = Gui(WIDTH, HEIGHT, game2)
gui1.run()
=======
game = Game([player1, player2, player3, player4, player5, player6], 0)
gui = Gui(WIDTH, HEIGHT, game)
gui.run()
>>>>>>> 06c1c6b4682d88ab2e448074b747e3a1b3543a0f
