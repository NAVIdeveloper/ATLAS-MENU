from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telebot
from webhooks.engine.manager import BotManager
from webhooks.master_bot.bot import staff
from webhooks import master_bot
from webhooks import engine
# Last line of imports

def initialize_telegram_bots():
    """Initialize bots at startup."""
    # engine.bot.initialize()
    # master_bot.bot.initialize()
initialize_telegram_bots()

def handle_webhook(request, bot):
    """Process incoming Telegram webhook updates."""
    if request.method == 'POST':
        try:
            json_str = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_str)
            bot.process_new_updates([update])
            return HttpResponse("ok")
        except Exception as error:
            print(error)
            return HttpResponse("error", status=500)
    return HttpResponse("error", status=400)

@csrf_exempt
def staff_webhook_view(request):
    return handle_webhook(request, staff)

@csrf_exempt
def engine_webhook_view(request, key):
    bot_instance = BotManager.get_bot(key)
    return handle_webhook(request, bot_instance.bot)
