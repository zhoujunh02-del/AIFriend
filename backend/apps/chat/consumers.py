import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from services.agent.agent import run_agent
from services.context.compressor import count_tokens, should_compress, compress, assemble_context
from apps.chat.models import ChatSession, Message
from services.voice_pipeline.pipeline import VoicePipeline

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.voice_pipeline = None
        await self.accept()
    
    async def disconnect(self, close_code):
        pass

    async def websocket_receive(self, message):                                                                                            
        if "bytes" in message:                                                                        
            await self.handle_audio(message["bytes"])
        else:                                                                                         
            await self.receive(message)
    
    async def handle_audio(self, audio_chunk: bytes):
        if self.voice_pipeline is None:
            session = await database_sync_to_async(ChatSession.objects.get)(id=self.session_id)
            persona = await database_sync_to_async(lambda: session.persona)()
            self.voice_pipeline = VoicePipeline(session, persona)
        
        result = await self.voice_pipeline.process_chunk(audio_chunk)
        if result is not None:
            await self.send(bytes_data=result)


    async def receive(self, text_data):
        data = json.loads(text_data)
        query = data["message"]
        session_id = data["session_id"]
        persona_prompt = data.get("persona_prompt", "You are a helpful assistant.")

        session = await database_sync_to_async(ChatSession.objects.get)(id=session_id)

        await database_sync_to_async(Message.objects.create)(
            session=session,
            role=Message.ROLE_USER,
            content=query,
            token_count=count_tokens(query),
        )
        needs_compress = await database_sync_to_async(should_compress)(session)
        if needs_compress:
            await database_sync_to_async(compress)(session)
        
        history = await database_sync_to_async(assemble_context)(session)

        loop = asyncio.get_running_loop()

        def send_token(token):
            asyncio.run_coroutine_threadsafe(
                self.send(json.dumps({"type": "token", "content": token})),
                loop
            )

        result = await asyncio.to_thread(
            run_agent, persona_prompt, query, [], history, send_token
        )

        answer = result["answer"]
        await database_sync_to_async(Message.objects.create)(
            session=session,
            role=Message.ROLE_ASSISTANT,
            content=answer,
            token_count=count_tokens(answer),
            function_calls_log=result["function_call_log"] or None,
        )

        await self.send(json.dumps({"type": "done", "function_calls_log": result["function_call_log"]}))
