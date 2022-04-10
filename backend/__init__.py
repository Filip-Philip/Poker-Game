from Hand import Hand
from Card import Card
from Suit import Suit
from Type import Type

# seven = [card6, card1, card2, card8, card7, card3, card9]
card1 = Card(Suit.CLUBS, Type.SIX)
card2 = Card(Suit.SPADES, Type.SIX)
card3 = Card(Suit.HEARTS, Type.KING)
card4 = Card(Suit.CLUBS, Type.JACK)
card5 = Card(Suit.CLUBS, Type.TEN)

card6 = Card(Suit.CLUBS, Type.SIX)
card7 = Card(Suit.SPADES, Type.SIX)
card8 = Card(Suit.CLUBS, Type.KING)
card9 = Card(Suit.HEARTS, Type.JACK)
card10 = Card(Suit.HEARTS, Type.NINE)

card11 = Card(Suit.CLUBS, Type.SIX)
card12 = Card(Suit.SPADES, Type.SIX)
card13 = Card(Suit.CLUBS, Type.SIX)
card14 = Card(Suit.HEARTS, Type.JACK)
card15 = Card(Suit.CLUBS, Type.NINE)

h1 = [card1, card2, card3, card4, card5]
hand1 = Hand()
hand1.cards = h1

h2 = [card6, card7, card8, card9, card10]
hand2 = Hand()
hand2.cards = h2

h3 = [card11, card12, card13, card14, card15]
hand3 = Hand()
hand3.cards = h3

# for card in h1:
#     print(card, end=' ')
# h1.sort()
# print()
# for card in h1:
#     print(card, end=' ')
# print()
# for card in h1:
#     print(card.type, card.type.next())


def print_hand(hand):
    for card in hand.cards:
        print(card.type, "of", card.suit, end='\t')
    print()


hands = [hand1, hand2, hand3]
# for h in hands:
#     print_hand(h)

hands.sort()

# print("-----")
# for h in hands:
#     print_hand(h)

big_hand = Hand()
han = Hand()
seven = [card15, card1, card12, card8, card7, card3, card9]
big_hand.cards = seven
han.choose_best(seven)
print_hand(big_hand)
print()
print_hand(han)


# print(hands[0].is_better_than(hands[1]))
# print(all(h1[i].type.next() == h1[i+1].type for i in range(len(h1) - 1)))
print()
print_hand(han)
print_hand(hand1)
print(han.is_better_than(hand1))
