from django.apps import AppConfig
import os

class WebhooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webhooks'

    # def ready(self):
    #     # # comment this condition and it's body in production 
    #     if os.environ.get('RUN_MAIN') == 'true':
    #         from webhooks.views import initialize_telegram_bots
    #         initialize_telegram_bots()
    #     # # uncomment in production this part
    #     # from webhooks.views import initialize_telegram_bots
    #     # initialize_telegram_bots()
