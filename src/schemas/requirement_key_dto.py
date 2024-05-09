from .base_dto import BaseDto 
from .key_dto import KeyDto
from .requirement_dto import RequirementDto

class RequirementKeyDto(BaseDto):
    requirement_id:int
    key_id :int
    requirement:RequirementDto
    key:KeyDto