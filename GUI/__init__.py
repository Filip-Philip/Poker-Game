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
#

game = Game([player1, player2, player3, player4], 0)
"""
card1 = Card(Suit.CLUBS, Type.QUEEN)
card2 = Card(Suit.CLUBS, Type.KING)
card3 = Card(Suit.CLUBS, Type.TWO)
card4 = Card(Suit.CLUBS, Type.FIVE)
card5 = Card(Suit.CLUBS, Type.THREE)
game.community_cards.append(card1)
game.community_cards.append(card2)
game.community_cards.append(card3)
game.community_cards.append(card4)
game.community_cards.append(card5)
"""
gui = Gui(WIDTH, HEIGHT, game)
gui.run()
