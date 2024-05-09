
from .base_repository import BaseRepository
from models import CompanySetting, Company, Function, FunctionKey, Requirement, RequirementKey
from core.exceptions import DataException
from sqlalchemy.orm import Session, joinedload, noload
from contextlib import AbstractContextManager
from typing import Callable
from core.logging import SolomindLogger 

class CompanySettingRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], logger:SolomindLogger):
        super().__init__(session_factory, logger)
    
    async def get(self, id:int) -> CompanySetting:
        with self.session_factory() as session:

            company_setting = session.query(CompanySetting)\
                .filter(CompanySetting.id == id).first()
            
            if company_setting :
                return company_setting
            else:
                raise DataException(f"CompanySetting with ID '{id}' could not be found.", error_code= "12002")
            
    async def get_by_company_id(self, company_id:int) -> CompanySetting:
        with self.session_factory() as session:

            company_setting = session.query(CompanySetting)\
                .options(joinedload(CompanySetting.company) .options(
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
                                ))\
                .filter(CompanySetting.company_id == company_id).first()
            
            if company_setting :
                return company_setting
            else:
                raise DataException(f"CompanySetting with ID '{company_id}' could not be found.", error_code= "12003")