import uuid
from django.db import models
from django.conf import settings
from apps.personas.models import Persona


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions",
    )
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="chat_sessions",
    )
    title = models.CharField(max_length=255, blank=True, default="")
    memory_summary = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} x {self.persona} ({self.id})"


class Message(models.Model):
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_ASSISTANT, "Assistant"),
    ]

    MODALITY_TEXT = "text"
    MODALITY_AUDIO = "audio"
    MODALITY_CHOICES = [
        (MODALITY_TEXT, "Text"),
        (MODALITY_AUDIO, "Audio"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    modality = models.CharField(max_length=10, choices=MODALITY_CHOICES, default=MODALITY_TEXT)
    content = models.TextField()
    audio_file_path = models.CharField(max_length=500, blank=True, default="")
    audio_duration_seconds = models.FloatField(null=True, blank=True)
    function_calls_log = models.JSONField(null=True, blank=True)
    token_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}"
