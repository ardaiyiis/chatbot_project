
from .base_dto import BaseDto 

class FileDto(BaseDto):
    name            :str
    content         :str
    file_extension  :str
    function_id     :int
