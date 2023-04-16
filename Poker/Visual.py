import abc
from Game import Game

class View(metaclass=abc.ABCMeta):
    """An interface for ViewDir."""
    @abc.abstractmethod
    def hello(self):
        """Greets the user and explains the rules."""
        pass

    @abc.abstractmethod
    def return_player_cards(self, name, cards):
        """Takes list of player's cards and return it in user's interface"""
        pass

    @abc.abstractmethod
    def return_board_cards(self, cards):
        """Takes list of player's cards and return it in user's interface"""
        pass

    @abc.abstractmethod
    def ask_for_players_num(self):
        """Reads command from user's interface"""
        pass

    @abc.abstractmethod
    def raise_error(self, data):
        """Takes error message and return it in user's interface."""
        pass

    @abc.abstractmethod
    def return_winners(self, winners):
        """Returns winners in user`s interface."""
        pass

    @abc.abstractmethod
    def return_loser(self, loser):
        """Returns loser in user`s interface."""
        pass

class ConsoleView(View):
    """This object can work with console."""

    def hello(self):
        print("Привет, друг!", '\n')
        print("Сейчас начнется игра в покер!")

    def ask_for_nickname(self):
        print("Введите свое имя:")
        return input()

    def ask_for_players_num(self):
        print("Сколько игроков будет с вами за столом? Не больше 3:")
        return int(input())

    def return_player_cards(self, name, cards):
        print(f"карты {name}:")
        print(*cards, sep=", ")

    def return_board_cards(self, cards):
        print("Карты на столе:")
        print(*cards)

    def ask_for_bid(self):
        print("Сделайте ставку:")
        return int(input())

    def raise_error(self, error_message):
        print('Ошибка.', end=' ')
        print(error_message)

    def return_winners(self, winners):
        print("Победили следующие игроки:")
        for comb, player in winners:
            print(player.name)

    def return_loser(self, loser):
        print(f"Игрок {loser.name} выбывает из игры")