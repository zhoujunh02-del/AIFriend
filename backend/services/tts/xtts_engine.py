from TTS.api import TTS
import io, scipy.io.wavfile as wav
import numpy as np

class XTTSEngine:
    def __init__(self):
        self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    
    def synthesize(self, text, speaker_wav, language="en"):
        audio = self.model.tts(
            text=text,
            speaker_wav=speaker_wav,
            language=language
        )
        buffer = io.BytesIO()
        wav.write(buffer, rate=24000, data=self.numpy_to_int16(audio))
        return buffer.getvalue()
    
    def numpy_to_int16(self, audio):
        return (np.array(audio) * 32767).astype(np.int16)



