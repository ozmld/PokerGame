import html

image_card_suit = {0: "♣️", 1: "♥️", 2: "♦️", 3: "♠️"}
image_card_value = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8",
                    9: "9", 10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"}

def get_start_message():
    return "Привет, друг!\nС помощью этого бота ты можешь играть в покер!"


def get_help_message():
    HELP_COMMAND = "<b>/start</b> - <em>запуск бота</em>" \
                   "\n<b>/help</b> - <em>список команд</em>" \
                   "\n<b>/description</b> - <em>описание работы бота</em>" \
                   "\n<b>/rules</b> - <em>правила покера</em>" \
                   "\n<b>/init_game</b> - <em>проинициализировать игру</em>" \
                   "\n<b>/start_game</b> - <em>начать игру</em>"
    return HELP_COMMAND


def get_description_message():
    description = """
    Привет!\nЗдесь ты можешь ознакомиться с ботом!\nС помощью
    этого бота ты сможешь играть в покер.\n Против тебя будут играть
    боты, в количестве до 4 штук. Сколько именно их будет, ты сможешь выбрать сам.
    Взаимодействие с ботом можно будет с помощью кнопок или просто сообщений, в зависимости
    от стадии игры.\nУдачи в игре!
    """
    return description


def get_rules_message():
    return "Можешь ознакомиться с " \
           "<a href=\"https://sugared-plywood-1cf.notion.site/Poker-rules-976f4240aa58491ebd3921844046ec0e\">" \
           "правилами покера</a>!"


def ask_ingame_name():
    text = "Привет! Прежде чем начать новую игру, определимся с твоим игровым именем!" \
           "\n(Просто напиши его в чат)"
    return text

def name_wrong_content_type_message():
    return "Отправь мне желаемое игровое имя текстом! Я не могу извлечь имя из" \
           "данного типа данных"


def get_name_clarify_message(name):
    name = html.escape(name)
    return f"Ваше игровое имя: <i>{name}</i>"

def get_name_set_message(name):
    #пользователь хочет установить такое имя
    name = html.escape(name)
    return f"Готово! Я вас запомнил. Ваше игровое имя: <i>{name}</i>"
def get_name_not_set_message():
    # пользователь не хочет устанавливать такое имя
    return "Хорошо, введите ваше имя еще раз."

def get_players_num_message(value):
    # сколько игроков 1-5
    return f"Игроков за столом: {value}"


def repr_card(card):
    return image_card_value[card.value] + image_card_suit[card.suit]


def get_cards_repr(cards):
    text = ""
    for card in cards:
        text += repr_card(card) + " "
    return text


def get_your_hand_repr(cards):
    return f"Ваша рука: {get_cards_repr(cards)}"

def get_player_hand_repr(name, cards):
    return f"Рука игрока: \"{name}\" {get_cards_repr(cards)}"

def ask_players_num_message():
    return f"Теперь опеделимся с количеством игроков!"
def get_players_num_message(players_num):
    # сколько игроков 1-5
    return f"Игроков за столом: {players_num}"


def get_init_game_ended_message():
    return f"Необходимые параметры заданы!" \
           f"\n\nНачнем играть -> /start_game"


def get_game_not_inited_message():
    return "Чтобы начать, нужно сначала определиться с игровыми параметрами:" \
           "\n->/init_game"


def get_game_start_message():
    return "Начинаем игру?"



def next_turn(turn: str):
    return ""


def get_notify_trade_state_message(cur_chips):
    return f"Время делать ставку! Ваш текущий банк: {cur_chips}"


def get_players_bids_message(players):
    text = ""
    for player in players.keys():
        text += f'{player.name} поставил {players[player]} фишек. (Остаток: {player.chips})\n'
    return text


def get_wrong_bid_fromat_message():
    return f"Прости, я тебя не понимаю. Чтобы сделать ставку - отправь число фишек," \
           f"которрое ты хочешь поставить!"


def get_winners_message(winners):
    text = ""
    if len(winners) == 1:
        text = "Победитель: "
    else:
        text = "Победители: "
    for comb, player in winners:
        text += player.name + "\n"
    return text


def get_player_zero_chips_message(name):
    return f"{name} выбывает! у него осталось 0 фишек"


def get_you_loose_message():
    return f"Вы проиграли! У Вас осталось 0 фишек"


def get_you_win_message():
    return f"Вы выиграли! У всех соперников осталось 0 фишек"


def get_game_quit_message():
    return "Выход из игры! " \
           "\n-> /start_game чтобы начать новую игру!"