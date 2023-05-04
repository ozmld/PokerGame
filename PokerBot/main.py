from create_bot import dp
from aiogram.utils import executor
from handlers import general
from PokerBot.database import sqlite_db


async def on_startup(_):
    print("Online")
    sqlite_db.sql_start()


general.register_handlers_general(dp)


try:
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
except:
    print("bad internet")