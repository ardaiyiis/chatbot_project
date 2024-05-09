
from .base_repository import BaseRepository
from models import Function, FunctionKey, File
from core.exceptions import DataException
from sqlalchemy.orm import Session, joinedload, noload
from contextlib import AbstractContextManager
from typing import Callable
from core.logging import SolomindLogger 

class FunctionRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], logger:SolomindLogger):
        super().__init__(session_factory, logger)
    
    async def get(self, id:int) -> Function:
        with self.session_factory() as session:

            function = session.query(Function)\
                .filter(Function.id == id).first()
            
            if function :
                return function
            else:
                raise DataException(f"Function with ID '{id}' could not be found.", error_code= "12004")
            
    async def get_by_company_id(self, company_id:int) -> Function:
        with self.session_factory() as session:

            function = session.query(Function)\
                            .options(
                                    joinedload(Function.keys)\
                                        .options(joinedload(FunctionKey.key))\
                                                # .options(joinedload(RequirementKey.requirement)
                                                #          .options(noload(Requirement.company)))                                  
                                    , joinedload(Function.data_library_type)
                                    , joinedload(Function.data_library).options(noload(File.function))
                            ).filter(Function.company_id == company_id).all()
            
            if function :
                return function
            else:
                raise DataException(f"CompanySetting with ID '{company_id}' could not be found.", error_code= "12005")