from openai import OpenAI
from core.logging import SolomindLogger
import time
import json

class AssistantService:
    def __init__(self, logger: SolomindLogger):
        self.logger = logger


    async def chat_with_assistant(self, thread_id, assistant_id, client)->json:
        run = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id=assistant_id,
        )


        while run.status != 'completed' or run.status == 'failed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(run.id, thread_id=thread_id)

    # Retrieve and return the latest message from the assistant
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        response = messages.data[0].content[0].text.value
        return response
    
    
    async def thread_message_update(self, client, thread_id, user_message):
        client.beta.threads.messages.create(thread_id=thread_id
                                           ,role="user",
                                           content=user_message)
        self.logger.get_logger(__name__).debug("Thread is updated. Thread_Id: %s", thread_id)
        return 
    
'''
    below code snippet can be used to use function_call feature within Assitant API:
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == 'completed':
                break
            elif run_status.status == 'requires_action':
                for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.function.name == "GeneralTours":
                        # Implement your function logic
                        arguments = json.loads(tool_call.function.arguments)
                        output = LibraryReaderService.library_reader('GeneralTours', **arguments)
                        client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id, run_id=run.id,
                                                                    tool_outputs=[{
                                                                        "tool_call_id": tool_call.id,
                                                                        "output": json.dumps(output)
                                                                    }])
                time.sleep(1)

'''

    