from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_start_game_keyboard():
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    continue_button = KeyboardButton(text="Продолжить")
    quit_button = KeyboardButton(text="Выйти")
    keyboard.add(continue_button, quit_button)
    return keyboard
