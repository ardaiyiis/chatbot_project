from openai import OpenAI
import json
from core.exceptions import DataException
from services import LibraryReaderService, ConfigService
from core.logging import SolomindLogger

class Chatbot:
    def __init__(self, config_service:ConfigService, library_reader_service:LibraryReaderService, logger: SolomindLogger):
        self.config_service:ConfigService = config_service
        self.config=self.config_service.config
        self.library_reader_service:LibraryReaderService = library_reader_service
        self.api_key = self.config.openai_api_key
        self.logger = logger
        
    def run_conversation(self, message_history, function_list):
        messages = message_history
        self.logger.get_logger(__name__).debug("Function List: %s", function_list)
        client = OpenAI(api_key=self.api_key)

        if function_list:
            response = client.chat.completions.create(
                model=self.config.model_name,
                temperature=self.config.temperature,
                messages=messages,
                functions=function_list,
                function_call="auto",
            )
        else:
            response = client.chat.completions.create(
                model=self.config.model_name,
                temperature=self.config.temperature,
                messages=messages,
            )
        response_message = response.choices[0].message

        if response_message.function_call:
            available_functions = {
                function["name"]: self.library_reader_service.library_reader for function in function_list
            }
            function_name = response_message.function_call.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message.function_call.arguments)

            self.logger.get_logger(__name__).debug("Function Name: %s", function_name)
            self.logger.get_logger(__name__).debug("Function Args: %s", function_args)
  

            function_response = function_to_call(function_name=function_name, **function_args)
            if not function_response:
                raise DataException(f"Function response could not be found.", error_code= "12009")
            self.logger.get_logger(__name__).debug("Function Response: %s", function_response)
            
            messages.append(response_message)
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
            second_response = client.chat.completions.create(
                model=self.config.model_name,
                temperature=self.config.temperature,
                messages=messages,
            )  # get a new response from GPT where it can see the function response
            self.logger.get_logger(__name__).debug("Function Response: %s", function_response)
            return second_response
        else:
            return response
