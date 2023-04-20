from Player import Player, Bot
from Deck import Combination, Card


def check_type(p):
    if type(p) is not Player and type(p) is not Bot:
        raise TypeError("Argument given is not a player")


class Board:
    players_in_game: list[Player]
    players_bids: dict[Player, int]
    begin_chips: int
    board: list[Card]
    highest_bid: int
    order: list[Player]
    bank: int

    def __init__(self, begin_chips=100):
        self.players_in_game = []
        self.players_bids = {}
        self.begin_chips = begin_chips
        self.board = []
        self.highest_bid = 0
        self.bank = 0

    def new_stage(self):
        self.highest_bid = 0

    def new_round(self):
        order = []
        order.extend(self.players_in_game)
        for player in self.get_players():
            self.players_bids[player] = 0

    def open_board_cards(self, cards):
        self.board.extend(cards)

    # Builder pattern
    def add_player(self, p: Player) -> None:
        check_type(p)
        self.players_bids[p] = 0
        self.players_in_game.append(p)
        p.chips = self.begin_chips

    def remove_player(self, p) -> None:
        check_type(p)
        try:
            self.players_bids.pop(p)
            self.players_in_game.remove(p)
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

    def get_players(self):
        return self.players_bids.keys()

    def deal_cards(self, cards):
        counter = 0
        for player in self.players_bids.keys():
            player.give_cards(cards[counter])
            counter += 1

    def hand_strength(self, player) -> Combination:
        if player not in self.get_players():
            raise KeyError("Argument given is not a player")
        hand = player.get_hand()
        combination = Combination(hand + self.board)
        combination.determine_strength()
        return combination

    def determine_winner(self) -> list[list[tuple[Combination, Player]]]:
        winners_temp = []

        for player in self.get_players():
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

    def split_bank(self, winners):
        # The main problem is that there can be many winners so we have to sort
        # them in increasing order according to their bids

        # Folders' bids we split between all winners
        folder_bank = 0
        for folder in self.get_players():
            if folder in self.players_in_game:
                continue
            folder_bank += self.players_bids[folder]
            self.players_bids[folder] = 0
        reward = folder_bank / len(winners)

        for winner in winners:
            winner.chips += reward

        winners_bid = {}
        for winner in winners:
            winners_bid[winner] = self.players_bids[winner]
        # Sorting winners in increasing their bids
        winners_bid = dict(sorted(winners_bid.items(), key=lambda item: item[1]))

        for cur_winner in winners_bid.keys():
            # Each winner can earn from every player not more than his bid
            win_bid = self.players_bids[cur_winner]

            # Evaluating sub_bank and decreasing players' bids (they give some chips to the sub_bank)
            sub_bank = 0
            for player in self.players_bids.keys():
                sub_bank += min(self.players_bids[player], win_bid)
                self.players_bids[player] -= min(self.players_bids[player], win_bid)
            reward = sub_bank / len(winners)

            # Each winner gain reward
            for winner in winners:
                winner.chips += reward
            # Remove current winner from list (because we handled him)
            winners.remove(cur_winner)
        # Return extra chips to players
        for player, chips in self.players_bids.items():
            player.chips += chips