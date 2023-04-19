from Deck import Deck
from Board import Board


class Game:
    def __init__(self, deck=Deck(), board=Board()):
        self.deck = deck
        self.deck.shuffle()
        self.board = board
        self.round = "preflop"
        self.round_num = 1
        self.round_flag = 1

    def next_stage(self):
        self.board.new_stage()
        if self.round_flag == 0:
            self.round_num += 1
            match self.round_num:
                case 1:
                    self.round = "preflop"
                case 2:
                    self.round = "flop"
                case 3:
                    self.round = "turn"
                case 4:
                    self.round = "river"
                case 5:
                    self.round = "showdown"
        else:
            self.round = "trade"
        self.round_flag = (self.round_flag + 1) % 2
class Round:
    def __init__(self, game=Game()):
        self.deck = game.deck
        self.board = game.board
    def open_card(self, number=1):
        cards_to_open = []
        for i in range(number):
            cards_to_open += self.deck.give_cards()
        self.board.open_board_cards(cards_to_open)


class PreFlop(Round):
    def distribution(self):
        number_players = self.board.get_players_number()
        cards = [self.deck.give_cards(2) for _ in range(number_players)]
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
        for player in self.board.players.keys():
            self.board.bid(player)