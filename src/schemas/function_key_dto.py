from typing import Optional
from .base_dto import BaseDto 
from .key_dto import KeyDto

class FunctionKeyDto(BaseDto): 
    function_id :int
    key_id :int
    key: Optional[KeyDto] = None 
    is_required : bool
