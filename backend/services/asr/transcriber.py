from faster_whisper import WhisperModel
import numpy as np


class WhisperTranscriber:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        self.model = WhisperModel(model_size, device, compute_type)
        
    
    def transcribe(self, audio_bytes, language="en") -> str:
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        segments, info = self.model.transcribe(audio_np, beam_size=5)

        return "".join(seg.text for seg in segments).strip()
