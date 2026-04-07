from .edge_tts_engine import EdgeTTSEngine
from .xtts_engine import XTTSEngine
import asyncio

class TTSRouter:
    def __init__(self):
        self.edge_engine = EdgeTTSEngine()
        self._xtts_engine = None
    
    def _get_xtts(self):
        if self._xtts_engine is None:
            self._xtts_engine = XTTSEngine()
        return self._xtts_engine
    
    async def synthesize(self, text: str, voice_profile) -> bytes:
        engine = voice_profile.engine
        if engine == voice_profile.ENGINE_EDGE_TTS:
            temp_engine = EdgeTTSEngine(voice=voice_profile.edge_voice_name, rate=voice_profile.edge_rate, volume=voice_profile.edge_volume)
            return await temp_engine.synthesize(text)
        elif engine == voice_profile.ENGINE_XTTS:
            temp_engine = self._get_xtts()
            result = await asyncio.to_thread(temp_engine.synthesize, text, voice_profile.xtts_speaker_embedding_path, voice_profile.xtts_language)
            return result


