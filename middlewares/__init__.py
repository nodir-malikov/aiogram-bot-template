from aiogram import Dispatcher
from loguru import logger
from middlewares.throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    logger.info("Подключение middlewares...")
    dp.middleware.setup(ThrottlingMiddleware())
