import json
import time
from openai import OpenAI
from services import ConfigService, CompanyService

class SingleRequestService:
    def __init__(self, company_service:CompanyService, config_service: ConfigService, logger):
        self.config_service:ConfigService = config_service
        self.config = self.config_service.config
        self.api_key = self.config.openai_api_key
        self.company_service = company_service
        self.logger = logger
        self.client = OpenAI(api_key=self.config.openai_api_key)


    async def request_with_assistant(self, item):
        company_settings = await self.company_service.get_company_setting(item.company_id)
        assistant_id = company_settings.company.assistant_id

        thread = self.client.beta.threads.create()
        thread_id = thread.id

        self.client.beta.threads.messages.create(thread_id=thread_id
                                           ,role="user",
                                           content=item.input_text)
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        while run.status != 'completed' or run.status == 'failed':
            time.sleep(1)
            run = self.client.beta.threads.runs.retrieve(run.id, thread_id=thread_id)

        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        response = messages.data[0].content[0].text.value
        self.logger.get_logger(__name__).debug("Assistant Response: %s", repr(messages.data[0].content[0]))
        return response

    async def request_with_gpt_4(self, item):
        try:
            # Getting formatter prompt from "prompts.py" file
            company_settings = await self.company_service.get_company_setting(item.company_id)
            system_prompt = company_settings.general_prompt


            completion = self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{item.input_text}"},
                ],
                temperature=0
            )

            response = json.loads(completion.choices[0].message.content)
            self.logger.get_logger(__name__).debug("GPT-4 Response: %s", response)
            return response

        except Exception as e:
            self.logger.get_logger(__name__).error("Error with GPT-4 request: %s", e)
            return None

