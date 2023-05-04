import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from PokerBot.create_bot import bot

from PokerBot.handlers.message_representings import *
from PokerBot.keyboard import *
from PokerBot.handlers.init_game import register_get_name_handlers, FSMGameInit

async def start_command(message: types.Message):
    start_message = get_start_message()
    await bot.send_message(message.chat.id, start_message, parse_mode="Markdown")


async def help_command(message: types.Message):
    help_message = get_help_message()
    await bot.send_message(message.chat.id, help_message, parse_mode="Markdown")





class FSMGame(StatesGroup):
    game_init = State()
    bid = State()
    preflop = State()
    flop = State()
    turn = State()
    river = State()
    showdown = State()


async def start_game(message: types.Message):
    text = ask_ingame_name()
    await bot.send_message(message.chat.id, text=text)
    await FSMGameInit.get_name.set()

async def name_incorrect(callback: types.CallbackQuery):
    print(10)
    await bot.send_message(callback.message.chat.id, "D")
    await callback.message.reply("t")
    await callback.answer()
async def get_name(message: types.Message):
    print(11)
    name = message.caption
    if message.content_type != 'text' and name is None:
        await message.reply(name_wrong_content_type_message())
        return
    elif message.content_type == 'text':
        name = message.text
    await message.reply(name_clarify(name), reply_markup=get_name_clarify_keyboard(), parse_mode='html')



def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])

    dp.register_message_handler(start_game, commands=['startgame'], state=None)

    register_get_name_handlers(dp)
