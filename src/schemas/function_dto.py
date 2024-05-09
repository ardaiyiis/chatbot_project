from .base_dto import BaseDto 
from .file_dto import FileDto 
from .data_library_type_dto import DataLibraryTypeDto
from .function_key_dto import FunctionKeyDto 
from typing import List, Optional

class FunctionDto(BaseDto):
    company_id:int
    name:str
    code:str
    description:str
    is_active:bool
    data_library_type_id:int 
    data_library_type:Optional[DataLibraryTypeDto] = None
    data_library:Optional[FileDto] = None
    keys:Optional[List[FunctionKeyDto]] = None