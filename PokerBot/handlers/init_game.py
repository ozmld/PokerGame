from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from PokerBot.create_bot import bot

from PokerBot.handlers.message_representings import *
from PokerBot.keyboard import *

from PokerBot.database import sqlite_db


class FSMGameInit(StatesGroup):
    get_name = State()
    clarify_name = State()
    get_players_num = State()


async def init_game(message: types.Message):
    sqlite_db.sql_add_user_command(message.from_user.id)
    text = ask_ingame_name()
    await bot.send_message(message.chat.id, text=text, parse_mode='html')
    await FSMGameInit.get_name.set()


async def get_name(message: types.Message, state: FSMContext):
    name = message.caption
    if message.content_type != 'text' and name is None:
        await message.reply(name_wrong_content_type_message(), parse_mode='html')
        return
    elif message.content_type == 'text':
        name = message.text
    await message.reply(get_name_clarify_message(name), reply_markup=get_name_clarify_keyboard(), parse_mode='html')
    await state.update_data(name=name)
    await state.set_state(FSMGameInit.clarify_name.state)

# async def name_correct(callback: types.CallbackQuery):


async def name_clarify(message: types.Message, state: FSMContext):
    if message.text == "Да":
        await bot.send_message(message.chat.id, get_name_set_message((await state.get_data())['name']),
                               reply_markup=types.ReplyKeyboardRemove(),
                               parse_mode='html')
        await FSMGameInit.get_players_num.set()
        await bot.send_message(message.chat.id, ask_players_num_message(),
                               reply_markup=get_players_num_keyboard(),
                               parse_mode='html')
    elif message.text == "Нет":
        await bot.send_message(message.chat.id, get_name_not_set_message(),
                               reply_markup=types.ReplyKeyboardRemove(),
                               parse_mode='html')
        await FSMGameInit.get_name.set()
    else:
        await bot.send_message(message.chat.id, "Прости, я не понимаю! Отправь мне \"Да\" или \"Нет\"",
                               parse_mode='html')


async def get_players_num(callback: types.callback_query, state: FSMContext):
    players_num = int(callback.data.split("_")[-1])
    await state.update_data(players_num=players_num)
    user_data = await state.get_data()
    sqlite_db.sql_update_user_command(callback.from_user.id, user_data['name'], user_data['players_num'])
    await state.finish()
    await callback.answer()
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=None,
                                        )
    await bot.send_message(callback.message.chat.id, get_players_num_message(players_num),
                           parse_mode='html')
    await bot.send_message(callback.message.chat.id, get_init_game_ended_message(),
                           parse_mode='html')
def register_init_game_handlers(dp: Dispatcher):
    dp.register_message_handler(init_game, commands=['init_game'])

    dp.register_message_handler(get_name, content_types=['any'], state=FSMGameInit.get_name)
    dp.register_message_handler(name_clarify, state=FSMGameInit.clarify_name)
    dp.register_callback_query_handler(get_players_num, state=FSMGameInit.get_players_num)
