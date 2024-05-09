from models import Company, CompanySetting
from data.repositories import CompanyRepository, CompanySettingRepository

class CompanyService:
    def __init__(self
                 , company_repository: CompanyRepository
                 , company_setting_repository: CompanySettingRepository):
        self.company_repository:CompanyRepository = company_repository
        self.company_setting_repository:CompanySettingRepository = company_setting_repository
    
    async def get_company(self, id:int) -> Company:
        return await self.company_repository.get(id)
    
    async def get_company_setting(self, company_id:int) -> CompanySetting:
        return await self.company_setting_repository.get_by_company_id(company_id)
    