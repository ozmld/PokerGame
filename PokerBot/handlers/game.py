from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from PokerBot.create_bot import bot

from PokerBot.handlers.message_representings import *
from PokerBot.keyboard import *

from PokerBot.database import sqlite_db

from Poker.Game import Game, PreFlop, Flop, Turn, River
from Poker.Player import Player, Bot
from Poker.Run import BOT_NAMES


class FSMGame(StatesGroup):
    trade = State()
    preflop = State()
    flop = State()
    turn = State()
    river = State()
    showdown = State()

    # def run_subround(self):
    #     match self._game.get_round_name():
    #         case "showdown":
    #             self._visual.return_board_cards(self._game.get_board_cards())
    #             for player in self._game.get_players():
    #                 self._visual.return_player_cards(player.get_name(), player.get_hand())
    #             winners = self._game.determine_winner()[-1]
    #             self._visual.return_winners(winners)
    #             winners = [winner for _, winner in winners]
    #             self._game.split_bank(winners)
    #         case "trade":
    #             self._visual.return_trade()
    #             for player in self._game.get_players():
    #                 if isinstance(player, Player) and not isinstance(player, Bot):
    #                     player.set_chips_to_bid(self._visual.ask_for_bid(player, self._game.get_bank()))
    #                 self._game.bid(player)
    #             self._visual.made_bids(self._game.players_bids())


async def start_game(message: types.Message, state: FSMContext):
    user_data = sqlite_db.sql_get_user_data_comman(message.from_user.id)
    name = user_data[1]
    players_num = int(user_data[2])
    if name == "" or players_num == "":
        await bot.send_message(message.chat.id, get_game_not_inited_message())
    else:
        game = Game()
        game.add_player(Player(name))
        for i in range(players_num):
            game.add_player(Bot(f"Бот {BOT_NAMES[i].capitalize()}"))
        await state.update_data(game=game)
        await state.set_state(FSMGame.preflop.state)
        await bot.send_message(message.chat.id, get_game_start_message(), reply_markup=get_start_game_keyboard())



async def trade(message: types.Message, state: FSMContext):
    pass


async def preflop(message: types.Message, state: FSMContext):
    game = (await state.get_data())['game']
    preflop = PreFlop(game)
    preflop.distribution()
    game.set_board(preflop.get_board())
    game.set_deck(preflop.get_deck())
    for player in game.get_players():
        if isinstance(player, Player) and not isinstance(player, Bot):
            await bot.send_message(message.chat.id,
                                   get_player_hand_message(player.get_name(), player.get_hand()))


async def flop(message: types.Message, state: FSMContext):
    game = (await state.get_data())['game']
    flop = Flop(game)
    flop.flop()
    game.set_board(flop.get_board())
    game.set_deck(flop.get_deck())
    await bot.send_message(message.chat.id, get_board_cards_message(game.get_board_cards()))
    await state.set_state(FSMGame.trade.state)


async def turn(message: types.Message, state: FSMContext):
    game = (await state.get_data())['game']
    turn = Turn(game)
    turn.turn()
    game.set_board(turn.get_board())
    game.set_deck(turn.get_deck())
    await bot.send_message(message.chat.id, get_board_cards_message(game.get_board_cards()))
    await state.set_state(FSMGame.trade.state)


async def river(message: types.Message, state: FSMContext):
    game = (await state.get_data())['game']
    river = River(game)
    river.river()
    game.set_board(river.get_board())
    game.set_deck(river.get_deck())
    await bot.send_message(message.chat.id, get_board_cards_message(game.get_board_cards()))
    await state.set_state(FSMGame.trade.state)


async def showdown(message: types.Message, state: FSMContext):
    await state.set_state(FSMGame.preflop.state)


async def quit_game(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, get_game_quit_message())


def register_game_handlers(dp: Dispatcher):
    dp.register_message_handler(start_game, commands=['start_game'])
    dp.register_message_handler(preflop, Text(equals="Продолжить"), state=FSMGame.preflop)
    dp.register_message_handler(flop, Text(equals="Продолжить"), state=FSMGame.flop)
    dp.register_message_handler(turn, Text(equals="Продолжить"), state=FSMGame.river)
    dp.register_message_handler(river, Text(equals="Продолжить"), state=FSMGame.trade)

    dp.register_message_handler(quit_game, Text(equals="Выйти"), state="*")
