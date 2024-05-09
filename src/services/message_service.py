from services import CompanyService, ConfigService, AssistantService
from schemas.requests import MessageProcessResponse, MessageProcessUsage
from data.repositories import MessageHistoryRepository
from openai import OpenAI

class MessageService:
    def __init__(self, company_service: CompanyService
                 , message_history_repository:MessageHistoryRepository
                 , config_service:ConfigService
                 , assistant_service:AssistantService):
        self.company_service:CompanyService = company_service
        self.message_history_repository:MessageHistoryRepository = message_history_repository
        self.assistant_service:AssistantService= assistant_service
        self.config_service:ConfigService = config_service
        self.config = self.config_service.config
        self.api_key = self.config.openai_api_key

    async def process(self, item):
        
        process_response = MessageProcessResponse()
        company_settings = await self.company_service.get_company_setting(item.company_id)

        client = OpenAI(api_key=self.config.openai_api_key)
        await self.message_history_repository.insert_message(item.user_session_key, role="user", content=item.input_text, company_id=item.company_id, client=client)
        conversation = await self.message_history_repository.get_latest_conversation(user_session_key=item.user_session_key, company_id=item.company_id)
        await self.assistant_service.thread_message_update(client, conversation.thread_id, item.input_text)
        response = await self.assistant_service.chat_with_assistant(client=client, thread_id=conversation.thread_id, assistant_id=company_settings.company.assistant_id)

        await self.message_history_repository.insert_message(item.user_session_key, role="assistant", content=response, company_id=item.company_id)        
        process_response.message = response

        process_response.usage = MessageProcessUsage(
            completion_tokens=0,
            prompt_tokens=0,
            total_tokens=0
        )
        return process_response
