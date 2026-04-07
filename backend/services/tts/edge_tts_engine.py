import edge_tts

class EdgeTTSEngine:
    def __init__(self, voice="ar-BH-LailaNeural", rate="+0%", volume="+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume
    
    async def synthesize(self, text: str) -> bytes:
        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
        buffer = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buffer.append(chunk["data"])
        
        return b"".join(buffer)
