from GUI.gui import Gui
from backend.game import Game
from backend.player import Player

if __name__ == "__main__":
    WIDTH, HEIGHT = 1500, 800
    player1 = Player("player1", 100)
    player2 = Player("player2", 100)
    player3 = Player("player3", 100)
    player4 = Player("player4", 100)
    player5 = Player("player5", 100)
    player6 = Player("player6", 100)
    #

    game1 = Game([player1, player2], 0)
    gui1 = Gui(WIDTH, HEIGHT, game1, main_player=player1, send_fun=print)
    gui1.run()
    game = Game([player1, player2, player3, player4, player5, player6], 0)
    gui = Gui(WIDTH, HEIGHT, game)
    gui.run()