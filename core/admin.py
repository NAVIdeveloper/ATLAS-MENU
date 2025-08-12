from django.contrib import admin
from core.models import (
    User,City,Language,
    EngineBotText,MasterBotText
)

# Register your models here.
admin.site.register(User)
admin.site.register(City)
admin.site.register(EngineBotText)
admin.site.register(MasterBotText)
admin.site.register(Language)
