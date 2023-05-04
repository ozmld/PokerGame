from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_name_clarify_keyboard():
    keyboard = ReplyKeyboardMarkup()
    yes_button = KeyboardButton(text="Да")
    no_button = KeyboardButton(text="Нет")
    keyboard.add(yes_button, no_button)
    return keyboard

def get_players_num_keyboard():
    keyboard = InlineKeyboardMarkup(one_time_keyboard=True)
    for players_num in range(1, 6):
        button = KeyboardButton(text=str(players_num), callback_data=f"players_{players_num}")
        keyboard.insert(button)
    return keyboard