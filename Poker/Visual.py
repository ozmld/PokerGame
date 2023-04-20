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
    def ask_for_repr_type(self):
        """Reads command from user's interface"""
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
    def kick_looser(self, loser):
        """Returns loser in user`s interface."""
        pass

class ConsoleView(View):

    string_card_suit = {0: " of clubs", 1: " of hearts", 2: " of diamonds", 3: " of spades"}
    string_card_value = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight",
                         9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}

    image_card_suit = {0: "♣", 1: "♥", 2: "♦", 3: "♠"}
    image_card_value = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8",
                        9: "9", 10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"}

    card_repr = {"cтроковый": (string_card_suit, string_card_value), "cимвольный": (image_card_suit, image_card_value)}
    """This object can work with console."""

    represent = "Стоковый"
    def get_available_represent_types(self):
        return self.card_repr.keys()

    def repr_card(self, card, repr_type):
        return self.card_repr[repr_type][1][card.value] + self.card_repr[repr_type][0][card.suit]

    def repr_cards(self, cards):
        return [self.repr_card(card, self.represent) for card in cards]

    def output(self, cards):
        print(*self.repr_cards(cards), sep=', ')

    def hello(self):
        print("Привет, друг!", '\n')
        print("Сейчас начнется игра в покер!")

    def ask_for_nickname(self):
        print("Введите свое имя:")
        return input()

    def ask_for_players_num(self):
        print("Сколько игроков будет с вами за столом? Не больше 3:")
        return int(input())

    def get_example(self, repr_type):
        return self.card_repr[repr_type][1][11] + self.card_repr[repr_type][0][1]

    def print_available_types(self, types):
        for i, repr_type in enumerate(types, start=1):
            print(f'{i}) {repr_type.capitalize()} ({self.get_example(repr_type)})')

    def ask_for_repr_type(self):
        print("Выберите тип представления карт из приведенных ниже:")

        types = list(self.get_available_represent_types())
        self.print_available_types(types)

        print("Можете просто ввести номер выбранного варианта")

        s = input()
        try:
            s = types[int(s) - 1]
        except IndexError:
            pass
        except ValueError:
            pass
        while s.lower() not in types:
            s = input("Такой тип вывода информации не поддерживается. Попробуй еще раз\n")
            try:
                s = types[int(s) - 1]
            except IndexError:
                pass
            except ValueError:
                pass
        print(f"Отлично! Вы выбрали {s.lower()} тип!\n")
        return s

    def return_player_cards(self, name, cards):
        print(f"карты {name}:")
        self.output(cards)

    def return_board_cards(self, cards):
        print("Карты на столе:")
        self.output(cards)

    def ask_for_bid(self, player, bank):
        print(f"Текущий банк: {bank} фишек")
        print(f"{player.name}, cделайте ставку. (Доступные фишки: {player.chips})")
        return int(input())

    def made_bids(self, players):
        for player in players.keys():
            print(f'{player.name} поставил {players[player]} фишек. (Остаток: {player.chips})')

    def raise_error(self, error_message):
        print('Ошибка.', end=' ')
        print(error_message)

    def return_winners(self, winners):
        print("Победили следующие игроки:")
        for comb, player in winners:
            print(player.name)

    def kick_looser(self, loser):
        print(f"Игрок {loser.name} остался без фишек. Он выбывает из игры")