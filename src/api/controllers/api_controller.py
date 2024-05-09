from fastapi_router_controller import Controller
from fastapi import APIRouter

__API_ROUTE_PREFIX__ = 'api'
class ApiController:
    @staticmethod
    def create(controller_name:str, openapi_tag:str = None) -> Controller:
        router = APIRouter(prefix=f'/{__API_ROUTE_PREFIX__}/{controller_name}', tags=[controller_name.title()])
        if(not openapi_tag):
            openapi_tag = controller_name
        controller = Controller(
            router,
            openapi_tag={
                "name": openapi_tag,
            },
        )
        return controller
    