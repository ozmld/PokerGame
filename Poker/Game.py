from Poker.Deck import Deck
from Poker.Board import Board


class Game:
    def __init__(self, deck=None, board=None):
        if deck is None:
            self.deck = Deck()
        else:
            self.deck = deck
        if board is None:
            self.board = Board()
        else:
            self.board = board
        self.deck.shuffle()
        self.round = "preflop"
        self.round_num = 0
        self.round_flag = 1

    def get_round_name(self):
        return self.round

    def set_board(self, another_board):
        self.board = another_board

    def set_round_num(self, num):
        self.round_num = num

    def get_round_num(self):
        return self.round_num

    def get_round(self):
        return self.round

    def set_deck(self, another_deck):
        self.deck = another_deck

    def remove_player(self, player):
        return self.board.remove_player(player)

    def bid(self, player):
        return self.board.bid(player)

    def split_bank(self, winners):
        return self.board.split_bank(winners)

    def determine_winner(self):
        return self.board.determine_winner()

    def get_players(self):
        return self.board.get_players()

    def get_bank(self):
        return self.board.bank

    def add_player(self, player):
        return self.board.add_player(player)

    def get_board_cards(self):
        return self.board.board

    def players_bids(self):
        return self.board.players_bids

    def next_round(self):
        self.board.new_round()
        self.deck = Deck()
        self.deck.shuffle()

    def next_stage(self):
        self.board.new_stage()
        if self.round_flag == 0:
            self.round_num = (self.round_num + 1) % 5
            match self.round_num:
                case 0:
                    self.round = "preflop"
                case 1:
                    self.round = "flop"
                case 2:
                    self.round = "turn"
                case 3:
                    self.round = "river"
                case 4:
                    self.round = "showdown"
        else:
            if self.round == "showdown":
                self.round = "preflop"
                self.round_flag = (self.round_flag + 1) % 2
            else:
                self.round = "trade"
        self.round_flag = (self.round_flag + 1) % 2


class Round:
    def __init__(self, game=Game()):
        self.deck = game.deck
        self.board = game.board

    def get_deck(self):
        return self.deck

    def get_board(self):
        return self.board

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
    pass
    # def show_cards(self):
    #     self.board.split_bank()


class Trade(Round):
    def notify_players(self):
        for player in self.board.get_players():
            self.board.bid(player)
