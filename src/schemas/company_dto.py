from .base_dto import BaseDto
from .function_dto import  FunctionDto
from .requirement_dto import RequirementDto
from typing import List, Optional

class CompanyDto(BaseDto):
    name:str
    code:str
    type_id:int
    logo:str 
    functions: Optional[List[FunctionDto]]
    requirements:Optional[List[RequirementDto]]