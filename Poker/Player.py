class Player:
    def __init__(self, name="NoName"):
        self.name = name
        self.chips = 0
        self.hand = []
        self.chips_to_bid = 0

    def change_chips(self, chips):
        self.chips += chips

    def give_cards(self, cards):
        for card in cards:
            self.hand.append(card)

    def make_bid(self, highest_bid):
        if self.chips_to_bid > self.chips:
            self.chips_to_bid = self.chips  # maybe do something else
        if highest_bid > self.chips and self.chips_to_bid != self.chips:
            raise Exception(f"Player {p.name} must go all-in to call bid")
        self.chips -= self.chips_to_bid
        return self.chips_to_bid
        # TODO: proceed def bid in class Game

    def get_hand(self):
        return self.hand


class Bot(Player):
    def make_bid(self, highest_bid):
        self.chips_to_bid = highest_bid
        if highest_bid > self.chips:
            self.chips_to_bid = self.chips
        self.chips -= self.chips_to_bid
        return self.chips_to_bid
    def change_strategy(self):
        ...
        # TODO: be able to change strategy of making decisions


class Rational(Bot):
    ...
    # TODO: describe strategy algorithm


class Agressive(Bot):
    ...
    # TODO: describe strategy algorithm
