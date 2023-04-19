from random import shuffle
from itertools import combinations


class Card:
    _repr = "string"
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        return self.value < other.value


class DeckIter:
    def __init__(self, deck_class, current_index=0):
        self._cards = deck_class.cards
        self._deck_size = len(deck_class.cards)
        self._current_index = current_index

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < self._deck_size:
            member = self._cards[self._current_index]
            self._current_index += 1
            return member
        raise StopIteration


class Deck:
    def __init__(self):
        self.cards = [Card(j, i) for i in range(4) for j in range(2, 15)]

    def shuffle(self):
        shuffle(self.cards)

    def __iter__(self):
        return DeckIter(self)

    def give_cards(self, number=1):
        return [self.cards.pop() for _ in range(number)]


class Combination:
    __combination_strength = {"royal_flush": 9, "straight_flush": 8, "four_of_a_kind": 7,
                              "full_house": 6, "flush": 5, "straight": 4, "three_of_a_kind": 3,
                              "two_pairs": 2, "pair": 1, "high_card": 0}
    __combination_len = 5
    pool: tuple
    name_of_highest_combination: str
    highest_combination: tuple
    kicker: tuple

    def __init__(self, pool):
        self.pool = tuple(pool)
        self.name_of_highest_combination = "None"  # name of combination
        self.highest_combination = ()  # combination itself (all cards in one set) (for high_card all 5 cards)
        self.kicker = ()  # other cards from 5 without combination

    def __lt__(self, other):
        if not isinstance(other, Combination):
            raise TypeError("Operand object type must be \"Combination\"")
        comb1_name = self.name_of_highest_combination
        comb2_name = other.name_of_highest_combination
        if comb1_name == "" == comb2_name:
            return False
        if comb1_name == "":
            return True
        if comb2_name == "":
            return False
        if self.__combination_strength[comb1_name] < self.__combination_strength[comb2_name]:
            return True
        if self.__combination_strength[comb1_name] > self.__combination_strength[comb2_name]:
            return False

        # Now we know that combinations are same
        values1 = sorted([elem.value for elem in self.highest_combination])
        values2 = sorted([elem.value for elem in other.highest_combination])
        kicker1 = sorted(self.kicker)
        kicker2 = sorted(other.kicker)
        match comb1_name:
            case "royal_flush":
                return False
            case "straight_flush" | "straight":
                if values2 == [2, 3, 4, 5, 14]:
                    return False
                if values1 == [2, 3, 4, 5, 14]:
                    return True
                return values1[-1] < values2[-1]
            case "four_of_a_kind" | "three_of_a_kind":
                return values1[0] < values2[0]
            case "full_house":
                return values1[2] < values2[2]
            case "flush" | "high_card":
                return values1[-1] < values2[-1]
            case "two_pairs":
                first_pair1_value = values1[0]
                second_pair1_value = values1[2]
                first_pair2_value = values2[0]
                second_pair2_value = values2[2]
                if second_pair1_value != second_pair2_value:
                    return second_pair1_value < second_pair2_value
                if first_pair1_value != first_pair2_value:
                    return first_pair1_value < first_pair2_value
                return kicker1 < kicker2
            case "pair":
                pair1_value = values1[0]
                pair2_value = values2[0]
                if pair1_value != pair2_value:
                    return pair1_value < pair2_value
                return kicker1 < kicker2

    def __eq__(self, other):
        if not isinstance(other, Combination):
            raise TypeError("Operand object type must be \"Combination\"")
        if self < other or other < self:
            return False
        if self.name_of_highest_combination == "" == other.name_of_highest_combination:
            return True
        values1 = [element.value for element in self.highest_combination + self.kicker]
        values2 = [element.value for element in other.highest_combination + other.kicker]
        if self.name_of_highest_combination == "flush":
            print(values1, values2)
        return sorted(values1) == sorted(values2)

    def determine_strength(self):
        def find_pair(cards) -> tuple:
            for combination in combinations(cards, 2):
                if len(set([card.value for card in combination])) == 1:
                    return combination
            return ()

        def find_two_pairs(cards) -> tuple:
            for combination in combinations(cards, 4):
                for first_pair in combinations(combination, 2):
                    second_pair = set(combination) - set(first_pair)
                    if find_pair(first_pair) and find_pair(second_pair):
                        return combination
            return ()

        def find_three_of_a_kind(cards) -> tuple:
            for combination in combinations(cards, 3):
                if len(set([card.value for card in combination])) == 1:
                    return combination
            return ()

        def find_straight(cards) -> tuple:
            for combination in combinations(cards, 5):
                values = sorted([card.value for card in combination])
                if values == [2, 3, 4, 5, 14] or set([values[i] - values[0] - i for i in range(5)]) == {0}:
                    return combination
            return ()

        def find_flush(cards) -> tuple:
            for combination in combinations(cards, 5):
                if len(set([card.suit for card in combination])) == 1:
                    return combination
            return ()

        def find_full_house(cards) -> tuple:
            for combination in combinations(cards, 5):
                for pair in combinations(combination, 2):
                    triple = set(combination) - set(pair)
                    if find_pair(pair) and find_three_of_a_kind(triple):
                        return combination
            return ()

        def find_four_of_a_kind(cards) -> tuple:
            for combination in combinations(cards, 4):
                if len(set([card.value for card in combination])) == 1:
                    return combination
            return ()

        def find_straight_flush(cards) -> tuple:
            for combination in combinations(cards, 5):
                if find_straight(combination) and find_flush(combination):
                    return combination
            return ()

        def find_royal_flush(cards) -> tuple:
            for combination in combinations(cards, 5):
                if sorted(list(combination))[0].value == 10 and find_straight_flush(combination):
                    return combination
            return ()

        all_hands = ["royal_flush", "straight_flush", "four_of_a_kind", "full_house",
                     "flush", "straight", "three_of_a_kind", "two_pairs", "pair"]
        combinations_finders = [find_royal_flush, find_straight_flush, find_four_of_a_kind, find_full_house,
                                find_flush, find_straight, find_three_of_a_kind, find_two_pairs, find_pair]
        self.pool = tuple(sorted(self.pool))
        for hand, combinations_finder in zip(all_hands, combinations_finders):
            if combinations_finder(self.pool):
                self.name_of_highest_combination, self.highest_combination = hand, combinations_finder(self.pool)
                kicker_temp = set(self.pool) - set(self.highest_combination)
                kicker_temp = sorted(kicker_temp)[-(self.__combination_len - len(self.highest_combination)):]
                self.kicker = tuple(kicker_temp)
                return
        self.name_of_highest_combination, self.kicker = "high_card", ()
        self.highest_combination = tuple(sorted(self.pool)[-self.__combination_len:])
