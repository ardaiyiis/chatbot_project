from schemas import MessageItem
import httpx
from httpx import Response
import json
from services import ConfigService
from services.message_service import MessageService
from core.logging import SolomindLogger

class GupshupService:
    def __init__(self, message_service:MessageService, config_service:ConfigService, logger:SolomindLogger):
        self.config_service:ConfigService = config_service
        self.config=self.config_service.config
        self.message_service:MessageService = message_service
        self.logger = logger
            
    async def process_message(self, request:dict):
        try:
            payload = request.get('payload', {})
            message_item = MessageItem(
                input_text=payload.get('payload', {}).get('text', ''),
                company_id=3,
                user_session_key=payload.get('sender', {}).get('phone', '')
            )
            response_text = await self.message_service.process(message_item)
            await self.send_response(response_text.message, message_item.user_session_key)
        except Exception as e:
            self.logger.get_logger(__name__).debug(f"Exception occured: {e}")

    async def send_response(self, message: dict, phone_number: str):
        url = "https://api.gupshup.io/sm/api/v1/msg"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "apikey": f"{self.config.gupshup_api_key}"
        }
        data = {
            "channel": "whatsapp", 
            "source": "908503407050",  
            "destination": phone_number,  
            "message": json.dumps(message),  
        }
        async with httpx.AsyncClient() as client:
            response: Response = await client.post(url, headers=headers, data=data)
            if response.is_success:
                self.logger.get_logger(__name__).debug(f"Message sent successfully: {data}")
            else:
                self.logger.get_logger(__name__).debug(f"Failed to send message: {response.status_code} - {response.text}")
