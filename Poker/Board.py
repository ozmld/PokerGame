from Player import Player


def check_type(p):
    if type(p) is not Player:
        raise TypeError("Argument given is not a player")


class Board:
    def __init__(self, begin_chips=100):
        self.players = {}
        self.begin_chips = begin_chips

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

    def bid(self, p, bid=0) -> None:
        # Player {p} bids {bid} chips
        check_type(p)
        try:
            self.players[p] += bid
        except KeyError:
            print("Player you want to add bid to is not in the players")

    def determine_winner(self) -> Player:
        # TODO: Check hands of all players and determine "win" hand
        # TODO: Return extra chips to "losers" ("winner" can not take "too much" chips)
        winner = self.players.get(0)
        return winner
