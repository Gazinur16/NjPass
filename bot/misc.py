import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils.executor import Executor
from config import TG_BOT_TOKEN
from db import Database

bot = Bot(token=TG_BOT_TOKEN, parse_mode=ParseMode.HTML)
bot_storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=bot_storage)
executor_ = Executor(dispatcher=dp, skip_updates=True)

logging.basicConfig(level=logging.INFO)
db = Database('database.db')
