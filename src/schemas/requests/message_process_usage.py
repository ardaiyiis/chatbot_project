from pydantic import BaseModel
from typing import List
class MessageProcessUsage:
    def __init__(self, total_tokens, prompt_tokens,completion_tokens) -> None:
        self.total_tokens = total_tokens
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
    
    total_tokens:int
    prompt_tokens :int
    completion_tokens:int