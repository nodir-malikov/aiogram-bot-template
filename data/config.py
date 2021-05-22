from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

I18N_DOMAIN = env.str("bot_username")
BASE_DIR = Path(__file__).parent
LOCALES_DIR = 'locales'

WEBHOOK_PATH = f'/bot/{BOT_TOKEN}'
WEBHOOK_URL = env.str("WEBHOOK_URL") + WEBHOOK_PATH
WEBAPP_HOST = env.str("WEBAPP_HOST")
WEBAPP_PORT = env.str("WEBAPP_PORT")

# Переключатель Вебхук режима
WEBHOOK = False
# Переключатель Дебаг режима
DEBUG = False
