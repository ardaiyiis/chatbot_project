
from .base_repository import BaseRepository
from models import Requirement, RequirementKey, Key
from core.exceptions import DataException
from sqlalchemy.orm import Session, noload
from contextlib import AbstractContextManager
from typing import Callable
from core.logging import SolomindLogger 

class RequirementRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], logger:SolomindLogger):
        super().__init__(session_factory, logger)
    
    async def get(self, id:int) -> Requirement:
        with self.session_factory() as session:

            requirement = session.query(Requirement)\
                .filter(Requirement.id == id).first()
            
            if requirement :
                return requirement
            else:
                raise DataException(f"Requirement with ID '{id}' could not be found.", error_code= "12006")
            
    async def get_by_key_name(self, key_name:str) -> Requirement:
        with self.session_factory() as session:

            requirement = session.query(Requirement)\
                            .options(noload(Requirement.company))\
                            .join(RequirementKey, Requirement.id == RequirementKey.requirement_id)\
                            .join(Key, RequirementKey.key_id == Key.id)\
                                .filter(Key.name == key_name).first()
            
            if requirement :
                return requirement
            else:
                return None