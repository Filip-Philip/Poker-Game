from functools import total_ordering
from Type import Type
from HandValues import HandValues
import operator
from itertools import permutations


@total_ordering
class Hand:
    FINAL_NUMBER_OF_CARDS = 5

    def __init__(self):
        self.cards = []

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            if len(self.cards) == len(other.cards) == self.FINAL_NUMBER_OF_CARDS:
                return self.is_better_than(other) == 0
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if len(self.cards) == len(other.cards) == self.FINAL_NUMBER_OF_CARDS:
                return self.is_better_than(other) == -1
        return NotImplemented

    def choose_best(self, seven_cards):
        possible_hands = list(permutations(seven_cards, r=self.FINAL_NUMBER_OF_CARDS))
        for index, possible_hand in enumerate(possible_hands):
            tmp = list(possible_hands[index])
            possible_hands[index] = Hand()
            possible_hands[index].cards = tmp

        self.cards = max(possible_hands).cards

    def all_are_same_suit(self):
        return all(x.suit == self.cards[0].suit for x in self.cards)

    def count_suit_groups(self):
        occurrences = [0] * (Type.ACE.value + 1)
        for card in self.cards:
            occurrences[card.type.value] += 1

        occurrences_and_types = []
        for index, occurrence_count in enumerate(occurrences):
            if occurrence_count > 0:
                occurrences_and_types.append((occurrence_count, index))
            # we sort by number_of_occurrences first and then by the value of the card
            occurrences_and_types.sort(reverse=True, key=operator.itemgetter(0, 1))
        return len(occurrences_and_types), occurrences_and_types

    def is_straight(self):
        self.cards.sort()
        return all(self.cards[i].type.next() == self.cards[i+1].type for i in range(len(self.cards) - 1))

    def is_royal_flush(self):
        if len(self.cards) == Hand.FINAL_NUMBER_OF_CARDS:
            if self.all_are_same_suit() and self.is_straight() and max(self.cards).type == Type.ACE:
                return True
        return False

    def is_straight_flush(self):
        if len(self.cards) == Hand.FINAL_NUMBER_OF_CARDS:
            if self.all_are_same_suit() and self.is_straight():
                return True
        return False

    def is_four_of_a_kind(self):
        if len(self.cards) == Hand.FINAL_NUMBER_OF_CARDS:
            n, occurrences = self.count_suit_groups()
            if n == 2:
                if occurrences[0][0] == 4:
                    return True
        return False

    def is_full_house(self):
        if len(self.cards) == Hand.FINAL_NUMBER_OF_CARDS:
            n, occurrences = self.count_suit_groups()
            if n == 2:
                highest_number_of_occurrences, second_highest_number_of_occurrences = occurrences[0][0], occurrences[1][0]
                if (highest_number_of_occurrences, second_highest_number_of_occurrences) == (3, 2):
                    return True
        return False

    def is_flush(self):
        if len(self.cards) == Hand.FINAL_NUMBER_OF_CARDS:
            if self.all_are_same_suit():
                return True
        return False

    def is_three_of_a_kind(self):
        if len(self.cards) == Hand.FINAL_NUMBER_OF_CARDS:
            n, occurrences = self.count_suit_groups()
            if n == 3:
                highest_number_of_occurrences = occurrences[0][0]
                if highest_number_of_occurrences == 3:
                    return True
        return False

    def is_two_pairs(self):
        if len(self.cards) == Hand.FINAL_NUMBER_OF_CARDS:
            n, occurrences = self.count_suit_groups()
            if n == 3:
                highest_number_of_occurrences, second_highest_number_of_occurrences = occurrences[0][0], occurrences[1][0]
                if (highest_number_of_occurrences, second_highest_number_of_occurrences) == (2, 2):
                    return True
        return False

    def is_pair(self):
        if len(self.cards) == Hand.FINAL_NUMBER_OF_CARDS:
            n, occurrences = self.count_suit_groups()
            if n == 4:
                highest_number_of_occurrences = occurrences[0][0]
                if highest_number_of_occurrences == 2:
                    return True
        return False

    def value(self):
        if len(self.cards) == Hand.FINAL_NUMBER_OF_CARDS:
            if self.is_royal_flush():
                return HandValues.ROYAL_FLUSH
            elif self.is_straight_flush():
                return HandValues.STRAIGHT_FLUSH
            elif self.is_four_of_a_kind():
                return HandValues.FOUR_OF_A_KIND
            elif self.is_full_house():
                return HandValues.FULL_HOUSE
            elif self.is_flush():
                return HandValues.FLUSH
            elif self.is_straight():
                return HandValues.STRAIGHT
            elif self.is_three_of_a_kind():
                return HandValues.THREE_OF_A_KIND
            elif self.is_two_pairs():
                return HandValues.TWO_PAIRS
            elif self.is_pair():
                return HandValues.PAIR
            else:
                return HandValues.HIGH_CARD

    def break_ties(self, other):
        n, occurrences = self.count_suit_groups()
        m, occurrences_other = other.count_suit_groups()
        if n == m:
            i = 0
            while i < n and occurrences[i][1] == occurrences_other[i][1]:
                i += 1

            if i == n:
                return 0
            elif occurrences[i][1] > occurrences_other[i][1]:
                return 1

            return -1

    def is_better_than(self, other):
        if self.__class__ is other.__class__:
            if self.value() == other.value():
                return self.break_ties(other)
            elif self.value() > other.value():
                return 1
            return -1

        return NotImplemented
