from fastapi_router_controller import Controller
from services.message_service import MessageService
from services.assistant_service import AssistantService
from services.single_request_service import SingleRequestService
from fastapi import Depends, BackgroundTasks
from schemas import MessageItem
from services.gupshup_service import GupshupService
from .api_controller import ApiController
from dependency_injector.wiring import Provide
from startup import Container

controller:Controller = ApiController.create('message')


@controller.use()
@controller.resource()
class MessageController:
    def __init__(self, message_service: MessageService = Depends(Provide[Container.message_service])
                 , guphup_service: GupshupService = Depends(Provide[Container.gupshup_service])
                 , single_request_service: SingleRequestService = Depends(Provide[Container.single_request_service])
                 , assistant_service:AssistantService = Depends(Provide[Container.assistant_service])):
        self.message_service = message_service
        self.gupshup_service = guphup_service
        self.assistant_service = assistant_service
        self.single_request_service = single_request_service

    @controller.route.post('/process')
    async def process(self, item: MessageItem):
        response = await self.message_service.process(item)
        # response = self.assistant_service.chat_with_assistant(item)
        return  response 

    @controller.route.post('/gupshup-webhook')
    async def gupshup_webhook(self, request: dict, background_tasks: BackgroundTasks):
        background_tasks.add_task(self.gupshup_service.process_message, request)
        # response = await self.gupshup_service.messager(request)
        return {"status": "Accepted", "code": 202}
    
    @controller.route.post('/single_request')
    async def ai_response(self, item: MessageItem):
        response = await self.single_request_service.request_with_assistant(item)
        return response