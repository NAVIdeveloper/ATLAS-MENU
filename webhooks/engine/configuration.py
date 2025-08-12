import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

WEBHOOK_BASE_URL = os.environ.get('WEBHOOK_BASE_URL')
TELEGRAM_URL = os.environ.get('TELEGRAM_BASE_URL')

URL_WEBHOOK_ENGINES = f"{WEBHOOK_BASE_URL}/{os.environ.get('URL_ENGINE')}"
URL_WEBHOOK_MENU = f"{WEBHOOK_BASE_URL}/template/menu"
URL_WEBHOOK_RETURN_ORDER = f"{WEBHOOK_BASE_URL}/order/return"

USERNAME_BOT_STAFF = os.environ.get('STAFF_USERNAME')
ENABLE_WEBHOOK = os.environ.get('ENABLE_ENGINE_WEBHOOK') == 'True'
if ENABLE_WEBHOOK:
    print('Engines are On...')
else:
    print('Engines are Off...')