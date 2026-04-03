import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from services.agent.agent import run_agent

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        query = data["message"]
        persona_prompt = data.get("persona_prompt", "You are a helpful assistant.")

        async def send_token(token):
            await self.send(json.dumps({"type": "token", "content": token}))
    
        result = await asyncio.to_thread(
            run_agent, persona_prompt, query, [], send_token
    )

        await self.send(json.dumps({"type": "done", "function_calls_log": result["function_call_log"]}))
