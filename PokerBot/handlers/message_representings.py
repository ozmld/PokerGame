import html
def get_start_message():
    pass


def get_help_message():
    pass


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

def get_name_set_message():
    # пользователь успешно установил имя
    return "test"
def get_name_not_set_message():
    # пользователь не хочет устанавливать такое имя
    return "test1"

def get_players_num_message():
    # сколько игроков 1-5
    return "?"
def name_another_name():
    pass


def next_turn():
    pass


def ask_for_bid():
    pass
