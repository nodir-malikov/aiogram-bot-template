import os
import time

from aiogram import executor, Dispatcher, types
from aiogram.types import AllowedUpdates
from loguru import logger

from loader import dp, db, bot, scheduler

# ============ THIS IS IMPORTANT ============
import middlewares, handlers, filters
# ============ ============ ============

from utils.notify_admins import notify_admins
from utils.set_bot_commands import set_default_commands
from aiogram.utils.executor import start_webhook

from data.config import WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK, ADMINS

# Если Вебхук
WEBHOOK_URL = WEBHOOK_URL
WEBAPP_HOST = WEBAPP_HOST
WEBAPP_PORT = int(WEBAPP_PORT)


async def send_db_to_admin():
    path_and_name = "data/main.db"

    date_and_time = time.ctime(os.path.getctime(path_and_name))

    await bot.send_document(chat_id=ADMINS[0], document=types.InputFile(path_and_name),
                            caption=f"Время создания:\n{date_and_time}")


def schedule_jobs():
    scheduler.add_job(func=send_db_to_admin, trigger="interval", hours=12, args=())


async def on_startup(dispatcher):
    schedule_jobs()  # Запуск планировшика задач

    # Переустанавливаем Вебхук
    logger.warning('Starting connection...')
    if WEBHOOK:
        await bot.delete_webhook()
        await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True, max_connections=100)

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляем про запуск
    await notify_admins()

    try:
        db.create_table_users()  # создаем БД если отсутствует
    except Exception as err:
        print(err)

    logger.info("Bot started successfully")


async def on_shutdown(dispatcher: Dispatcher) -> None:
    logger.warning('Bye!')
    # Закрытие Вебхука.
    if WEBHOOK:
        await bot.delete_webhook()

    # Закрытие соединения с БД
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    scheduler.start()  # Запуск заплонированных задач

    # Если не нужен Вебхук
    if not WEBHOOK:
        executor.start_polling(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=False,
            allowed_updates=AllowedUpdates.MESSAGE + AllowedUpdates.EDITED_MESSAGE + AllowedUpdates.CALLBACK_QUERY,
        )
    else:
        # Если нужен Вебхук
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            allowed_updates=AllowedUpdates.MESSAGE + AllowedUpdates.EDITED_MESSAGE + AllowedUpdates.CALLBACK_QUERY,
            skip_updates=False,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )

# установка вебхука
# https://api.telegram.org/bot1877485677:AAFwGRM_ccJ0Wody1BtgbiAthBPf0QEvDUM/setWebhook?url=https://webhook.site/7f27b7bd-8891-493c-a62a-2597b1a50d6e

# удаление вебхука
# https://api.telegram.org/bot1877485677:AAFwGRM_ccJ0Wody1BtgbiAthBPf0QEvDUM/deleteWebhook?url=https://webhook.site/7f27b7bd-8891-493c-a62a-2597b1a50d6e