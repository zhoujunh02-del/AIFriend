from celery import shared_task
from TTS.api import TTS
import torch
import os
from django.utils import timezone
from apps.voice.models import VoiceCloneJob

@shared_task
def clone_voice(job_id):
    job = VoiceCloneJob.objects.get(id=job_id)
    job.status = job.STATUS_PROCESSING
    job.save()

    try:
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        gpt_cond_latent, speaker_embedding = tts.synthesizer.tts_model.get_conditioning_latents(audio_path=job.reference_audio_path)
        
        save_path = job.reference_audio_path.replace(".wav", "_embedding.pt")
        torch.save(speaker_embedding, save_path)
        job.voice_profile.xtts_speaker_embedding_path = save_path
        job.voice_profile.save()

        job.status = job.STATUS_COMPLETED
        job.completed_at = timezone.now()
        job.save()
    except Exception as e:
        job.status = job.STATUS_FAILED
        job.error_message = str(e)
        job.save()
        return
    
