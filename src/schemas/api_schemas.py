from pydantic import BaseModel

class MessageItem(BaseModel):
    input_text: str
    company_id: int
    user_session_key: str

