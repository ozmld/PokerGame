import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from PokerBot.create_bot import bot

from PokerBot.handlers.message_representings import *
from PokerBot.keyboard import *
from PokerBot.handlers.init_game import register_init_game_handlers, FSMGameInit
from PokerBot.handlers.game import register_game_handlers
async def start_command(message: types.Message):
    start_message = get_start_message()
    await bot.send_message(message.chat.id, start_message, parse_mode="Markdown")


async def help_command(message: types.Message):
    help_message = get_help_message()
    await bot.send_message(message.chat.id, help_message, parse_mode="Markdown")




def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])

    register_init_game_handlers(dp)
    register_game_handlers(dp)
