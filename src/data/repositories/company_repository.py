
from .base_repository import BaseRepository
from models import Company, Function, FunctionKey, Requirement, RequirementKey
from core.exceptions import DataException
from sqlalchemy.orm import joinedload, Session, noload
from contextlib import AbstractContextManager
from typing import Callable
from core.logging import SolomindLogger 
class CompanyRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], logger:SolomindLogger):
        super().__init__(session_factory, logger)
    
    async def get(self, id: str) -> Company:
        with self.session_factory() as session:
            
            #company = session.query(Company).join(Company.functions).filter(Company.id == id).first()
            
            # company = session.query(Company) \
            #                 .options(
            #                         joinedload(Company.functions)\
            #                         .options( 
            #                                    joinedload(Function.keys).options(noload(FunctionKey.key))\
            #                                  , noload(Function.data_library_type)\
            #                                  , noload(Function.data_library)#.options(joinedload(File.function))
            #                                 )\
            #                         , noload(Company.requirements)
            #                         , noload(Company.type)
            #                     ).filter(Company.id == id).first()


            company = session.query(Company) \
                            .options(
                                    joinedload(Company.functions)\
                                            .options( 
                                                joinedload(Function.keys).options(joinedload(FunctionKey.key))\
                                                , joinedload(Function.data_library_type)\
                                                , joinedload(Function.data_library)
                                                )\
                                    , joinedload(Company.requirements)\
                                            .options(noload(Requirement.company)\
                                                     , joinedload(Requirement.keys).options(joinedload(RequirementKey.key))
                                                     )
                                    , joinedload(Company.type)
                                ).filter(Company.id == id).first()
        
            if company : 
                return company
            else: 
                raise DataException(f"Company with ID '{id}' could not be found.", error_code= "12001")

