from .base_dto import BaseDto 
class RequirementDto(BaseDto):
    company_id          : int
    name                : str
    code                : str
    description         : str
    is_active           : bool
    question_to_user    : str
