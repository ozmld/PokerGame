import asyncio

from aiogram import types, Dispatcher

from PokerBot.create_bot import bot

from PokerBot.database import sqlite_db

from PokerBot.handlers.message_representings import *
from PokerBot.handlers.init_game import register_init_game_handlers, FSMGameInit
from PokerBot.handlers.game import register_game_handlers


async def start_command(message: types.Message):
    sqlite_db.sql_add_user_command(message.from_user.id)
    start_message = get_start_message()
    await bot.send_message(message.chat.id, start_message, parse_mode="html")


async def help_command(message: types.Message):
    help_message = get_help_message()
    await bot.send_message(message.chat.id, help_message, parse_mode="html")


async def description_command(message: types.Message):
    description_message = get_description_message()
    await bot.send_message(message.chat.id, description_message, parse_mode="html")


async def rules_command(message: types.Message):
    rules_message = get_rules_message()
    await bot.send_message(message.chat.id, rules_message, parse_mode="html")


def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(description_command, commands=['description'])
    dp.register_message_handler(rules_command, commands=['rules'])

    register_init_game_handlers(dp)
    register_game_handlers(dp)
