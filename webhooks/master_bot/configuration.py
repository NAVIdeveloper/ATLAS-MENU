import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

STAFF_BOT_TOKEN = os.environ.get('STAFF_BOT_TOKEN')
USERNAME_BOT_STAFF = os.environ.get('STAFF_USERNAME')

WEBHOOK_URL = f"{os.environ.get('WEBHOOK_BASE_URL')}/{os.environ.get('URL_STAFF')}"
TELEGRAM_URL = os.environ.get('TELEGRAM_BASE_URL')
JOIN_GROUP_URL = f"{TELEGRAM_URL}/{os.environ.get('URL_STAFF')}?startgroup=admin"

ENABLE_WEBHOOK = os.environ.get('ENABLE_STAFF_WEBHOOK') == 'True'
if ENABLE_WEBHOOK:
    print('Staff Bot is On...')
else:
    print('Staff Bot is Off...')