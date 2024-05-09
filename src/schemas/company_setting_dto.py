
from .company_dto import CompanyDto
from .base_dto import BaseDto
from typing import Optional
class CompanySettingDto(BaseDto): 
    company_id:int
    company:Optional[CompanyDto] = None
    name_of_the_bot:str
    general_prompt:str
    welcome_message:str
