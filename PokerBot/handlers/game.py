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


async def start_game(message: types.Message, state: FSMContext):
    user_data = sqlite_db.sql_get_user_data_comman(message.from_user.id)[0]
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


async def preflop(message: types.Message, state: FSMContext):
    game = (await state.get_data())['game']
    preflop = PreFlop(game)
    preflop.distribution()
    game.set_board(preflop.get_board())
    game.set_deck(preflop.get_deck())
    game.next_stage()
    for player in game.get_players():
        if isinstance(player, Player) and not isinstance(player, Bot):
            await bot.send_message(message.chat.id,
                                   get_your_hand_repr(player.get_hand()),
                                   reply_markup=get_trade_keyboard(get_cards_repr(player.get_hand())),
                                   )
            await state.update_data(player_hand=get_cards_repr(player.get_hand()))
            await state.update_data(player_chips=player.get_chips())
    await state.update_data(next_state=FSMGame.flop.state)
    await state.update_data(game=game)
    await state.set_state(FSMGame.trade.state)

    user_data = await state.get_data()
    await bot.send_message(message.chat.id, get_notify_trade_state_message(user_data['player_chips']),
                           reply_markup=get_player_hand_keyboard(user_data['player_hand']),
                           )


async def flop(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    game = user_data['game']
    player_hand = user_data['player_hand']
    player_chips = user_data['player_chips']

    flop = Flop(game)
    flop.flop()
    game.set_board(flop.get_board())
    game.set_deck(flop.get_deck())
    game.next_stage()
    await state.update_data(game=game)
    await state.update_data(next_state=FSMGame.turn.state)
    await state.set_state(FSMGame.trade.state)
    await bot.send_message(message.chat.id, get_cards_repr(game.get_board_cards()))
    await bot.send_message(message.chat.id, get_notify_trade_state_message(player_chips),
                           reply_markup=get_player_hand_keyboard((await state.get_data())['player_hand']),
                           )


async def turn(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    game = user_data['game']
    player_hand = user_data['player_hand']
    player_chips = user_data['player_chips']

    turn = Turn(game)
    turn.turn()
    game.set_board(turn.get_board())
    game.set_deck(turn.get_deck())
    game.next_stage()
    await bot.send_message(message.chat.id, get_cards_repr(game.get_board_cards()),
                           reply_markup=get_trade_keyboard(player_hand),
                           )

    await state.update_data(next_state=FSMGame.river.state)
    await state.update_data(game=game)

    await state.set_state(FSMGame.trade.state)
    await bot.send_message(message.chat.id, get_notify_trade_state_message(player_chips),
                           reply_markup=get_player_hand_keyboard((await state.get_data())['player_hand']),
                           )


async def river(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    game = user_data['game']
    player_hand = user_data['player_hand']
    player_chips = user_data['player_chips']

    river = River(game)
    river.river()
    game.set_board(river.get_board())
    game.set_deck(river.get_deck())
    game.next_stage()
    await bot.send_message(message.chat.id, get_cards_repr(game.get_board_cards()),
                           reply_markup=get_trade_keyboard(player_hand),
                           )
    await state.update_data(next_state=FSMGame.showdown.state)
    await state.update_data(game=game)

    await state.set_state(FSMGame.trade.state)
    await bot.send_message(message.chat.id, get_notify_trade_state_message(player_chips),
                           reply_markup=get_player_hand_keyboard((await state.get_data())['player_hand']),
                           )


async def showdown(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    game = user_data['game']
    player_hand = user_data['player_hand']
    player_chips = user_data['player_chips']

    game.next_stage()

    for player in game.get_players():
        await bot.send_message(message.chat.id, get_player_hand_repr(player.get_name(), player.get_hand()))
    winners = game.determine_winner()[-1]
    await bot.send_message(message.chat.id, get_winners_message(winners),
                           reply_markup=get_next_round_keyboard())
    winners = [winner for _, winner in winners]
    game.split_bank(winners)
    game.next_round()
    def human_is_in_game(game):
        for player in game.get_players():
            if type(player) is not Bot and type(player) is Player:
                return True
        return False
    async def delete_zero_balance_players(game):
        players = list(game.get_players())
        for player in players:
            if player.get_chips() == 0:
                await bot.send_message(message.chat.id, get_player_zero_chips_message(player.name))
                game.remove_player(player)
    if not human_is_in_game(game):
        await bot.send_message(message.chat.id, get_you_loose_message())
        return
    if len(game.get_players()) == 1:
        await bot.send_message(message.chat.id, get_you_win_message())
        return
    await delete_zero_balance_players(game)
    await state.update_data(game=game)
    await state.set_state(FSMGame.preflop.state)


async def trade(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    game = user_data['game']
    player_hand = user_data['player_hand']
    next_state = user_data['next_state']

    chips_to_bid = message.text
    if not chips_to_bid.isdecimal():
        await bot.send_message(message.chat.id, get_wrong_bid_fromat_message(),
                               reply_markup=get_player_hand_keyboard(player_hand),
                               )
        return
    chips_to_bid = int(chips_to_bid)
    for player in game.get_players():
        if isinstance(player, Player) and not isinstance(player, Bot):
            player.set_chips_to_bid(chips_to_bid)
            game.bid(player)
            await state.update_data(player_chips=player.get_chips())
        else:
            game.bid(player)
    await state.set_state(next_state)
    await state.update_data(game=game)
    await bot.send_message(message.chat.id, get_players_bids_message(game.players_bids()),
                           reply_markup=get_trade_keyboard(player_hand),
                           )


async def quit_game(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, get_game_quit_message())


def register_game_handlers(dp: Dispatcher):
    dp.register_message_handler(quit_game, Text(equals="Выйти"), state="*")

    dp.register_message_handler(start_game, commands=['start_game'])
    dp.register_message_handler(preflop, Text(equals="Начать игру"), state=FSMGame.preflop)
    dp.register_message_handler(preflop, Text(equals="Новый раунд"), state=FSMGame.preflop)

    dp.register_message_handler(flop, Text(equals="Продолжить"), state=FSMGame.flop)
    dp.register_message_handler(turn, Text(equals="Продолжить"), state=FSMGame.turn)
    dp.register_message_handler(river, Text(equals="Продолжить"), state=FSMGame.river)
    dp.register_message_handler(showdown, Text(equals="Продолжить"), state=FSMGame.showdown)

    dp.register_message_handler(trade, state=FSMGame.trade)
