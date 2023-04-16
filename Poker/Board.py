from Player import Player, Bot
from Deck import Combination, Card


def check_type(p):
    if type(p) is not Player and type(p) is not Bot:
        raise TypeError("Argument given is not a player")


class Board:
    players: dict[Player, int]
    begin_chips: int
    board: list[Card]

    def __init__(self, begin_chips=100):
        self.players = {}
        self.begin_chips = begin_chips
        self.board = []

    def open_board_cards(self, cards):
        for card in cards:
            self.board.append(card)

    # Builder pattern
    def add_player(self, p) -> None:
        check_type(p)
        self.players[p] = 0

    def remove_player(self, p) -> None:
        check_type(p)
        try:
            self.players.pop(p)
        except KeyError:
            print("Player you want to remove is not in the players")

    def bid(self, p: Player, bid=0) -> None:
        # Player {p} bids {bid} chips
        check_type(p)
        try:
            self.players[p] += bid
            p.make_bid(bid)
        except KeyError:
            print("Player you want to add bid to is not in the players")

    def get_players_number(self):
        return len(self.players)

    def deal_cards(self, cards):
        counter = 0
        for player in self.players.keys():
            player.give_cards(cards[counter])
            counter += 1

    def hand_strength(self, player) -> Combination:
        if player not in self.players.keys():
            raise KeyError("Argument given is not a player")
        hand = player.get_hand()
        combination = Combination(hand + self.board)
        combination.determine_strength()
        return combination

    def determine_winner(self) -> list[list[tuple[Combination, Player]]]:
        winners_temp = []
        for player in self.players:
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