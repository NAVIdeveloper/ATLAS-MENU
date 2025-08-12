from django.urls import path
from webhooks.views import *

urlpatterns = [
    path("webhook/bot/staff/",staff_webhook_view,name='staff-webhook'),
    path("webhook/bot/engine/<key>/",engine_webhook_view,name='engine-webhook'),
]