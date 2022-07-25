from django.db import models

class TelegramChatsView(models.Model):
    chat_name = models.CharField(max_length=100)
    title = models.TextField(blank=True)
    body = models.TextField(blank=True)
    time_of_public = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
