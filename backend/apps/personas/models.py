import uuid
from django.db import models
from django.conf import settings
from apps.voice.models import VoiceProfile
from apps.knowledge.models import KnowledgeBase


class Persona(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True, default="")
    personality_prompt = models.TextField()
    backstory = models.TextField(blank=True, default="")
    greeting_template = models.CharField(max_length=500, default="Hello! How can I help you today?")
    avatar_url = models.URLField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_personas",
    )
    voice_profile = models.OneToOneField(
        VoiceProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="persona",
    )
    knowledge_base = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="personas",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
