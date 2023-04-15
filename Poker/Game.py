from Deck import Deck
from Board import Board


class Game:
    def __init__(self, deck=Deck(), board=Board()):
        self.deck = deck
        self.board = board


class Round(Game):
    def open_card(self, number=1):
        cards_to_open = []
        for i in range(number):
            cards_to_open.append(self.deck.give_cards())
        self.board.open_board_cards(cards_to_open)


class PreFlop(Round):
    def distribution(self):
        number_players = self.board.get_players_number()
        cards = [[self.deck.give_cards(2)] for _ in range(number_players)]
        self.board.deal_cards(cards)


class Flop(Round):
    def flop(self):
        self.open_card(3)


class Turn(Round):
    def turn(self):
        self.open_card(1)


class River(Round):
    def river(self):
        self.open_card(1)


class ShowDown(Round):
    def show_cards(self):
        self.board.split_bank()


class Trade(Round):
    def notify_players(self):
        ...
        # TODO: notify players that trade round began
