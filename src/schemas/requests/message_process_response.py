from pydantic import BaseModel
from typing import List
from .message_process_usage import MessageProcessUsage
class MessageProcessResponse:
    message:str = None
    usage:MessageProcessUsage = None