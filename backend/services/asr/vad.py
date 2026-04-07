import torch
import numpy as np
torch.set_num_threads(1)

class SileroVAD:
    def __init__(self, threshold=0.5, sampling_rate=16000, chunk_size=512):
        self.threshold = threshold
        self.sampling_rate = sampling_rate
        self.chunk_size = chunk_size

        self.model, utils = torch.hub.load(
        repo_or_dir='snakers4/silero-vad',                                                            
        model='silero_vad',
        force_reload=False                                                                            
        )
        (self.get_speech_timestamps, _, self.read_audio, _, _) = utils


    def is_speech(self, audio_chunk: bytes) -> bool:
        # bytes → numpy → tensor
        audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
        tensor = torch.tensor(audio_np)
        confidence = self.model(tensor, self.sampling_rate).item()
        return confidence >= self.threshold
    
    def collection_until_silence(self, audio_chunks: list[bytes], silence_duration=0.8) -> bytes:
        silent_chunks = 0
        silence_threshold = int(silence_duration * self.sampling_rate / self.chunk_size)
        
        for i, chunk in enumerate(audio_chunks):
            if not self.is_speech(chunk):
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks >= silence_threshold:
                return b"".join(audio_chunks[:i+1])
            
    
        return b"".join(audio_chunks)