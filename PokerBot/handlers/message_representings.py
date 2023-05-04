import html
def get_start_message():
    return "Привет, друг!\nС помощью этого бота ты можешь играть в покер!"


def get_help_message():
    HELP_COMMAND = """
    <b>/start</b> - <em>запуск бота</em>
    <b>/help</b> - <em>список команд</em>
    <b>/description</b> - <em>описание работы бота</em>
    """
    return HELP_COMMAND


def get_description():
    description = """
    Привет!\nЗдесь ты можешь ознакомиться с ботом!\nС помощью
    этого бота ты сможешь играть в покер.\n Против тебя будут играть
    боты, в количестве до 4 штук. Сколько именно их будет, ты сможешь выбрать сам.
    Взаимодействие с ботом можно будет с помощью кнопок или просто сообщений, в зависимости
    от стадии игры.\nУдачи в игре!
    """
    return description
def get_rules_message():
    return "С правилами покера можешь ознакомиться по ссылке:"


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


def ask_players_num_message():
    return f"Теперь опеделимся с количеством игроков!"
def get_players_num_message(players_num):
    # сколько игроков 1-5
    return f"Игроков за столом: {players_num}"


def get_init_game_ended_message():
    return f"Необходимые параметры заданы!" \
           f"\n\nНачнем играть -> /start_game"


def get_game_not_inited_message():
    return "test"


def get_game_start_message():
    return "tester"


def get_player_hand_message(name, hand):
    print(name, hand)
    return "Рука"


def next_turn(turn: str):
    return ""


def ask_for_bid():
    return "Время делать ставку!"


def get_game_quit_message():
    return "выход"
