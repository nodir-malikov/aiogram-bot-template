from aiogram_broadcaster import TextBroadcaster
from data.config import ADMINS


async def notify_admins():
    await TextBroadcaster(ADMINS, 'The bot is running!').run()
