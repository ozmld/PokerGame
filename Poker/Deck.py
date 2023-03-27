from random import shuffle
card_suit = {0: "clubs", 1: "hearts", 2: "diamonds", 3: "spades"}
card_value = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight",
              9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return card_value[self.value] + " of " + card_suit[self.suit]


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

    def give_card(self):
        return self.cards.pop()