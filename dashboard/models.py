from django.db import models


class TelegramChat(models.Model):
    CHAT_TYPES = (
        ("channel", "Channel"),
        ("group", "Group"),
        ("supergroup", "Supergroup"),
    )

    tg_id = models.BigIntegerField(unique=True)
    type = models.CharField(max_length=20, choices=CHAT_TYPES)

    title = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    members_count = models.IntegerField(null=True, blank=True)
    last_checked_message_id = models.BigIntegerField(null=True, blank=True)

    is_safe = models.BooleanField(default=False)
    risk_score = models.FloatField(default=0.0)

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

    def __str__(self):
        return f"{self.title} ({self.type})"
