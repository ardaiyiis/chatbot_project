
from services import CompanyService
from fastapi import Depends
from dependency_injector.wiring import Provide
from startup import Container
from .api_controller import ApiController
from fastapi_router_controller import Controller
from schemas import CompanyDto, CompanySettingDto
from automapper import mapper
from schemas.requests import CompanyGetRequest, CompanySettingGetRequest
controller:Controller = ApiController.create('company')


@controller.use()
@controller.resource()
class CompanyController:
    def __init__(self,  company_service:CompanyService = Depends(Provide[Container.company_service])):
        self.company_service = company_service

    @controller.route.post("/get")
    async def get(self,request:CompanyGetRequest):
        company = await self.company_service.get_company(request.id)
        company_dto = mapper.to(CompanyDto).map(company)
        #company_dto= CompanyDto.from_orm(company)
        return company_dto
    
    @controller.route.post("/setting/get", response_model=CompanySettingDto)
    async def get_setting(self,request:CompanySettingGetRequest)->CompanySettingDto:
        company_setting = await self.company_service.get_company_setting(request.id)
        company_setting_dto = mapper.to(CompanySettingDto).map(company_setting)
        #company_dto= CompanyDto.from_orm(company)
        return company_setting_dto
    