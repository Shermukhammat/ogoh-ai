from django.contrib import admin
from .models import TelegramChat



@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    pass
