import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from services.agent.agent import run_agent
from services.context.compressor import count_tokens, should_compress, compress, assemble_context
from apps.chat.models import ChatSession, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        pass

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

        loop = asyncio.get_event_loop()

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
