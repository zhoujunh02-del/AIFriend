from services.asr.vad import SileroVAD                                                            
from services.asr.transcriber import WhisperTranscriber
from services.tts.tts_router import TTSRouter                                                     
from services.rag.pipeline import rag_query                                                       
from services.agent.agent import run_agent                                                        
from services.rag.retriever import HybridRetriever                                                
from services.rag.reranker import BGEReranker     
from apps.chat.models import ChatSession                                                          
from apps.personas.models import Persona
import asyncio 

class VoicePipeline:
    def __init__(self, session, persona):
        self.silerovad = SileroVAD()
        self.whispertranscriber = WhisperTranscriber()
        self.ttsrouter = TTSRouter()

        self.session = session                                                   
        self.persona = persona

        self.audio_buffer = []
        self.silent_chunks = 0

    async def process_chunk(self, audio_chunk: bytes) ->bytes | None:
        self.audio_buffer.append(audio_chunk)
        silence_threshold = int(0.8 * self.silerovad.sampling_rate / self.silerovad.chunk_size)
        if not self.silerovad.is_speech(audio_chunk):
            self.silent_chunks += 1
            if self.silent_chunks >= silence_threshold:
                self.silent_chunks = 0
                audio_out = await self._process_speech()
                self.audio_buffer = []
                return audio_out
            else:
                return None
        else:
            self.silent_chunks = 0

    
    async def _process_speech(self) -> bytes:
        audio_bytes = b"".join(self.audio_buffer)
        text = self.whispertranscriber.transcribe(audio_bytes)      # user_prompt
        persona_prompt = self.persona.personality_prompt                 # persona_prompt

        retriever = HybridRetriever(self.persona.knowledge_base.chroma_collection_name, [])
        reranker = BGEReranker()
        rag_context = rag_query(persona_prompt, text, retriever, reranker, top_k=3)
        result = await asyncio.to_thread(run_agent, self.persona.personality_prompt, text,rag_context, [], None)
        answer = result["answer"]

        audio_out = await self.ttsrouter.synthesize(answer, self.persona.voice_profile)
        return audio_out