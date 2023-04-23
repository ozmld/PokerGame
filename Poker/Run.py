from Game import *
from Visual import ConsoleView
from Player import Player, Bot

#TODO distinguish players in round and players in game

BOT_NAMES = ["Виталий", "Михаил", "Кирилл"]


class Run:
    def __init__(self):
        self._visual = ConsoleView()
        self._game = Game()

    def convert_int_repr(self, repr_type):
        types = list(self._visual.get_available_represent_types())
        try:
            repr_type = types[int(repr_type) - 1]
        except IndexError:
            pass
        except ValueError:
            pass
        return repr_type
    def check_repr_type(self, repr_type):
        types = list(self._visual.get_available_represent_types())
        repr_type = self.convert_int_repr(repr_type)
        return repr_type.lower() in types
    def start(self):
        self._visual.hello()
        name = self._visual.ask_for_nickname()
        self._game.add_player(Player(name))
        repr_type = self._visual.ask_for_repr_type()
        while not self.check_repr_type(repr_type):
            self._visual.raise_error("Выбранного Вами типа не существует!")
            repr_type = self._visual.ask_for_repr_type()
        repr_type = self.convert_int_repr(repr_type)
        self._visual.set_represent(repr_type)
        players_num = self._visual.ask_for_players_num()

        while not players_num.isnumeric() or int(players_num) < 0 or int(players_num) > 3:
            self._visual.raise_error("Количество игроков должно быть натуральным числом, не большим 3!")
            players_num = self._visual.ask_for_players_num()
        players_num = int(players_num)
        for i in range(players_num):
            self._game.add_player(Bot(f"Бот {BOT_NAMES[i]}"))

    def run_subround(self):
        match self._game.get_round_name():
            case "preflop":
                preflopp = PreFlop(self._game)
                preflopp.distribution()
                self._game.set_board(preflopp.get_board())
                self._game.set_deck(preflopp.get_deck())
                for player in self._game.get_players():
                    if not isinstance(player, Bot):
                        self._visual.return_player_cards(player.get_name(), player.get_hand())
            case "flop":
                flopp = Flop(self._game)
                flopp.flop()
                self._game.set_board(flopp.get_board())
                self._game.set_deck(flopp.get_deck())
                self._visual.return_board_cards(self._game.get_board_cards())
            case "turn":
                turnn = Turn(self._game)
                turnn.turn()
                self._game.set_board(turnn.get_board())
                self._game.set_deck(turnn.get_deck())
                self._visual.return_board_cards(self._game.get_board_cards())
            case "river":
                riverr = River(self._game)
                riverr.river()
                self._game.set_board(riverr.get_board())
                self._game.set_deck(riverr.get_deck())
                self._visual.return_board_cards(self._game.get_board_cards())
            case "showdown":
                self._visual.return_board_cards(self._game.get_board_cards())
                for player in self._game.get_players():
                    self._visual.return_player_cards(player.get_name(), player.get_hand())
                winners = self._game.determine_winner()[-1]
                self._visual.return_winners(winners)
                winners = [winner for _, winner in winners]
                self._game.split_bank(winners)
            case "trade":
                self._visual.return_trade()
                for player in self._game.get_players():
                    if isinstance(player, Player) and not isinstance(player, Bot):
                        player.set_chips_to_bid(self._visual.ask_for_bid(player, self._game.get_bank()))
                    self._game.bid(player)
                self._visual.made_bids(self._game.players_bids())

    def next_subround(self):
        self._game.next_stage()

    def next_round(self):
        self._visual.new_round()
        self._game.next_round()

    def delete_zero_balance_players(self):
        players = list(self._game.get_players())
        for player in players:
            if player.get_chips() == 0:
                self._visual.kick_looser(player)
                self._game.remove_player(player)

    def checker_subround_num(self):
        return self._game.get_round_num()

    def human_is_in_game(self):
        for player in self._game.get_players():
            if type(player) is not Bot and type(player) is Player:
                return True
        return False

    def get_players_num(self):
        return len(self._game.get_players())

    def get_subround_name(self):
        return self._game.get_round()

    def end_game(self):
        if self.get_players_num() > 1:
            self._visual.return_end_lose()
        else:
            self._visual.return_end(list(self._game.get_players())[0])
