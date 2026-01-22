from django.db import models
from django.utils import timezone


class TelegramChat(models.Model):
    CHAT_TYPES = (
        ("channel", "Channel"),
        ("group", "Group"),
        ("supergroup", "Supergroup")
    )

    tg_id = models.BigIntegerField(unique=True, null=True, blank=True)
    type = models.CharField(max_length=20, choices=CHAT_TYPES)

    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    members_count = models.IntegerField(default=0, blank=True, null=True)

    last_checked_message_id = models.BigIntegerField(null=True, blank=True)
    risk = models.CharField(max_length=20,
                            choices=(
                                ("safe", "Safe"),
                                ("risky", "Risky"),
                                ("unknown", "Unknown"),
                            ),
                            default="unknown"
                            )

    discovered_by = models.CharField(
        max_length=50,
        choices=(
            ("admin_query", "Admin Query"),
            ("forward", "Forwarded Post"),
            ("mention", "Mention"),
            ("link", "Invite Link"),
        ),
        default="admin_query",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_checked_at = models.DateTimeField(default=timezone.now)
    listening = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.type})"


class TgUser(models.Model):
    tg_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} (@{self.username or 'no_username'})"
    

class WarningMessage(models.Model):
    chat = models.ForeignKey(TelegramChat, on_delete=models.CASCADE)
    message_id = models.BigIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WarningMessage {self.message_id} in chat {self.chat.tg_id}"