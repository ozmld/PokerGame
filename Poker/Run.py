from Game import *
from Visual import ConsoleView
from Player import Player, Bot

#TODO distinguish players in round and players in game

BOT_NAMES = ["Виталий", "Михаил", "Кирилл"]
class Run:
    def __init__(self):
        self._visual = ConsoleView()
        self._game = Game()

    def start(self):
        self._visual.hello()
        name = self._visual.ask_for_nickname()
        self._game.board.add_player(Player(name))
        type = self._visual.ask_for_repr_type()
        self._visual.represent = type
        num = self._visual.ask_for_players_num()
        while (not isinstance(num, int)) or num < 0 or num > 3:
            self._visual.raise_error("Неверный тип данных.")
            num = self._visual.ask_for_players_num()
        for i in range(num):
            self._game.board.add_player(Bot(f"Бот {BOT_NAMES[i]}"))

    def run_subround(self):
        match self._game.round:
            case "preflop":
                preflopp = PreFlop(self._game)
                preflopp.distribution()
                self._game.board = preflopp.board
                self._game.deck = preflopp.deck
                # self._game.round.distribution()
                for player in self._game.board.get_players():
                    if not isinstance(player, Bot):
                        self._visual.return_player_cards(player.name, player.hand)
            case "flop":
                flopp = Flop(self._game)
                flopp.flop()
                self._game.board = flopp.board
                self._game.deck = flopp.deck
                self._visual.return_board_cards(self._game.board.board)
            case "turn":
                turnn = Turn(self._game)
                turnn.turn()
                self._game.board = turnn.board
                self._game.deck = turnn.deck
                self._visual.return_board_cards(self._game.board.board)
            case "river":
                riverr = River(self._game)
                riverr.river()
                self._game.board = riverr.board
                self._game.deck = riverr.deck
                self._visual.return_board_cards(self._game.board.board)
            case "showdown":
                #self._game.round.show_cards()
                self._visual.return_board_cards(self._game.board.board)
                for player in self._game.board.get_players():
                    self._visual.return_player_cards(player.name, player.hand)
                winners = self._game.board.determine_winner()[-1]
                self._visual.return_winners(winners)
                winners = [winner for _, winner in winners]
                self._game.board.split_bank(winners)
            case "trade":
                print("Время делать ставку!")
                # self._visual.ask_for_bid(list(self._game.board.players.keys())[1])
                for player in self._game.board.get_players():
                    if isinstance(player, Player) and not isinstance(player, Bot):
                        player.chips_to_bid = self._visual.ask_for_bid(player, self._game.board.bank)
                    self._game.board.bid(player)
                self._visual.made_bids(self._game.board.players_bids)
                # TODO send player`s bid to ??
                # TODO process bots

    def next_subround(self):
        self._game.next_stage()

    def delete_zero_balance_players(self):
        for player in self._game.board.players.keys():
            if player.chips == 0:
                self._visual.kick_looser(player.name)
                self._game.board.remove_player(player)

    def checker_subround_num(self):
        return self._game.round_num

    def PlayerIsInGame(self):
        pass
        #TODO