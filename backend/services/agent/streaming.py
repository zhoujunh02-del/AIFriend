from langchain_core.callbacks import BaseCallbackHandler

class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self, send_token_func):
        self.send_token_func = send_token_func
    
    def on_llm_new_token(self, token, **kwargs):
        self.send_token_func(token)
        