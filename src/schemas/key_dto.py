from .base_dto import BaseDto  

class KeyDto(BaseDto):
    company_id :int
    name : str
    code : str
    description : str
    type : str