from django.conf import settings
from django.db import models


class Conversation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations"
    )
    title = models.CharField(max_length=120, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        indexes = [
            models.Index(fields=["user", "-updated_at"]),
        ]

    def __str__(self) -> str:
        label = self.title.strip() or f"Conversa #{self.pk}"
        return f"{label} ({self.user})"


class Message(models.Model):
    class Role(models.TextChoices):
        SYSTEM = "system", "system"
        USER = "user", "user"
        ASSISTANT = "assistant", "assistant"

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=16, choices=Role.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]
        indexes = [
            models.Index(fields=["conversation", "created_at"]),
            models.Index(fields=["conversation", "id"]),
        ]

    def __str__(self) -> str:
        preview = self.content.strip().replace("\n", " ")
        if len(preview) > 60:
            preview = preview[:57] + "..."
        return f"{self.role}: {preview}"

