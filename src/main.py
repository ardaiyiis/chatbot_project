import uvicorn 
from schemas import MessageItem
from a2wsgi import ASGIMiddleware
from services import ConfigService
from pydantic import BaseModel 
from services.config_service import ConfigService
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
import environment
from startup import SolomindeApi, Container 
from fastapi_router_controller import Controller
from core.logging import SolomindLogger



configService = ConfigService()
class PromptItem(BaseModel):
    system_prompt: str
class GetCompanyRequest(BaseModel):
    company_id: int


environment.DEBUG = True
app = SolomindeApi.create_app()
logger = app.container.logger().get_logger(__name__)

logger.info(f"{app.title} is intializing modules.")
app.container.wire(modules=[__name__, 'api.controllers'])

for router in Controller.routers():
    app.include_router(router)
logger.info(f"{app.title} started.")
uvicorn.run(app, host="0.0.0.0", port=8000)
