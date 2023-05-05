import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from create_bot import dp
from aiogram.utils import executor
from handlers import general
from database import sqlite_db


async def on_startup(_):
    print("Online")
    sqlite_db.sql_start()


general.register_handlers_general(dp)


try:
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
except:
    print("bad internet")