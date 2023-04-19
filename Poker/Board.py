from Player import Player, Bot
from Deck import Combination, Card


def check_type(p):
    if type(p) is not Player and type(p) is not Bot:
        raise TypeError("Argument given is not a player")


class Board:
    players: list[Player]
    players_bids: dict[Player, int]
    begin_chips: int
    board: list[Card]
    highest_bid: int
    order: list[Player]
    bank: int

    def __init__(self, begin_chips=100):
        self.players = []
        self.players_bids = {}
        self.begin_chips = begin_chips
        self.board = []
        self.highest_bid = 0
        self.bank = 0

    def new_stage(self):
        self.highest_bid = 0

    def new_round(self):
        order = []
        order.extend(self.players)
        for player in self.players:
            self.players_bids[player] = 0

    def open_board_cards(self, cards):
        for card in cards:
            self.board.append(card)

    # Builder pattern
    def add_player(self, p: Player) -> None:
        check_type(p)
        self.players_bids[p] = 0
        self.players.append(p)
        p.chips = self.begin_chips

    def remove_player(self, p) -> None:
        check_type(p)
        try:
            self.players_bids.pop(p)
        except KeyError:
            print("Player you want to remove is not in the players")

    def bid(self, p: Player) -> None:
        # Player {p} bids {bid} chips
        check_type(p)
        try:
            bid = p.make_bid(self.highest_bid)
            self.players_bids[p] += bid
            self.highest_bid = max(self.highest_bid, bid)
            self.bank += bid
        except KeyError:
            raise KeyError("Player you want to add bid to is not in the players")

    def get_players_number(self):
        return len(self.players_bids)

    def deal_cards(self, cards):
        counter = 0
        for player in self.players_bids.keys():
            player.give_cards(cards[counter])
            counter += 1

    def hand_strength(self, player) -> Combination:
        if player not in self.players_bids.keys():
            raise KeyError("Argument given is not a player")
        hand = player.get_hand()
        combination = Combination(hand + self.board)
        combination.determine_strength()
        return combination

    def determine_winner(self) -> list[list[tuple[Combination, Player]]]:
        winners_temp = []

        for player in self.players_bids:
            winners_temp.append((self.hand_strength(player), player))
        winners_temp = sorted(winners_temp, key=lambda x: x[0])
        winners = [[winners_temp[0]]]
        for i in range(1, len(winners_temp)):
            if winners_temp[i][0] == winners[-1][-1][0]:
                winners[-1].append(winners_temp[i])
            else:
                winners.append([winners_temp[i]])
        # list where [i] element is list of player with (i + 1)-th strength of hand
        return winners

    def split_bank(self):
        winners = self.determine_winner()
        self.highest_bid = 0