from django.contrib import admin
from .models import TelegramChat, WarningMessage



@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    pass


@admin.register(WarningMessage)
class WarningMessageAdmin(admin.ModelAdmin):
    pass
