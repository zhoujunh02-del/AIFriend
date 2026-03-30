import uuid
from django.db import models


class VoiceProfile(models.Model):
    ENGINE_EDGE_TTS = "edge_tts"
    ENGINE_XTTS = "xtts_v2"
    ENGINE_CHOICES = [
        (ENGINE_EDGE_TTS, "Edge TTS"),
        (ENGINE_XTTS, "XTTS v2 (Voice Clone)"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    engine = models.CharField(max_length=20, choices=ENGINE_CHOICES, default=ENGINE_EDGE_TTS)

    # Edge TTS fields
    edge_voice_name = models.CharField(max_length=100, default="en-US-AriaNeural")
    edge_rate = models.CharField(max_length=20, default="+0%")
    edge_volume = models.CharField(max_length=20, default="+0%")

    # XTTS v2 fields
    xtts_speaker_embedding_path = models.CharField(max_length=500, blank=True, default="")
    xtts_language = models.CharField(max_length=10, default="en")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.engine} - {self.edge_voice_name}"


class VoiceCloneJob(models.Model):
    STATUS_QUEUED = "queued"
    STATUS_PROCESSING = "processing"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_QUEUED, "Queued"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voice_profile = models.ForeignKey(VoiceProfile, on_delete=models.CASCADE, related_name="clone_jobs")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUED)
    reference_audio_path = models.CharField(max_length=500)
    error_message = models.TextField(blank=True, default="")
    celery_task_id = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"CloneJob {self.id} - {self.status}"
