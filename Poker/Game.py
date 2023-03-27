from Deck import Deck


class Game:
    def __init__(self, deck):
        self.deck = deck


class Round(Game):
    ...


class PreFlop(Round):
    def distribution(self):
        ...
        # TODO: deal 2 cards to each player and 5 close cards on board


class Flop(Round):
    def flop(self):
        ...
        # TODO: open first 3 cards


class Turn(Round):
    def turn(self):
        ...
        # TODO: open 4-th cards


class River(Round):
    def river(self):
        ...
        # TODO: open 5-th card


class ShowDown(Round):
    def show_cards(self):
        ...
        # TODO: notify that round ended and we should distribute the winner


class Trade(Round):
    def notify_players(self):
        ...
        # TODO: notify players that trade round began