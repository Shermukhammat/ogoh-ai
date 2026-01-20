from django.db import models


class Query(models.Model):
    data = models.CharField(max_length=255, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Channel(models.Model):
    tg_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True, null=True)
    last_checked_message_id = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    safe_channel = models.BooleanField(default=False)

    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='channels')

    def __str__(self):
        return self.name