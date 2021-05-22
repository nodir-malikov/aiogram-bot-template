from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiograph import Telegraph
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config

from middlewares.language_middleware import setup_middleware

from utils.db_api.sqlite import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(path_to_db="data/main.db")
telegraph = Telegraph()
scheduler = AsyncIOScheduler()

# Настроим i18n middleware для работы с многоязычностью
i18n = setup_middleware(dp)

# Создадим псевдоним для метода gettext
_ = i18n.gettext  # Это для кнопок и текстов, которые находятся в самих хэдлерах
__ = i18n.lazy_gettext  # Это для кнопок, которые находятся в отдельных файлах
