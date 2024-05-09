
from pydantic import BaseModel

class BaseDto(BaseModel):
    id:int

    class Config:
        orm_mode = True