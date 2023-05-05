from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_start_game_keyboard():
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    continue_button = KeyboardButton(text="Начать игру")
    quit_button = KeyboardButton(text="Выйти")
    keyboard.add(continue_button, quit_button)
    return keyboard


def get_trade_keyboard(hand_cards):
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    hand_button = KeyboardButton(text=f"Ваша рука: {hand_cards}")
    continue_button = KeyboardButton(text="Продолжить")
    quit_button = KeyboardButton(text="Выйти")
    keyboard.add(hand_button)
    keyboard.add(continue_button, quit_button)
    return keyboard


def get_player_hand_keyboard(hand_cards):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    hand_button = KeyboardButton(text=f"Ваша рука: {hand_cards}")
    keyboard.add(hand_button)
    return keyboard


def get_next_round_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    new_round_button = KeyboardButton(text=f"Новый раунд")
    quit_button = KeyboardButton(text="Выйти")

    keyboard.add(new_round_button, quit_button)
    return keyboard

