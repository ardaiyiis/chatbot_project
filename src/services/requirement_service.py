from data.repositories import RequirementRepository
from datetime import date


class RequirementService:
    def __init__(self, requirement_repository:RequirementRepository):
        self.requirement_repository:RequirementRepository = requirement_repository

    async def create_requirement_key_dictionary(self, function_list):
        requirement_key_dictionary = {}
        
        for function in function_list:
            function_name = function["name"]
            required_keys = function["parameters"]["required"]
            function_requirements = {}
            
            for key_name in required_keys:
                # You may need to query the database to fetch the associated Requirement
                requirement = await self.requirement_repository.get_by_key_name(key_name)
                if requirement and requirement.question_to_user is not None:
                    function_requirements[key_name] = requirement.question_to_user
            
            if function_requirements:  # Check if the dictionary is not empty
                requirement_key_dictionary[function_name] = function_requirements
            
        '''{required_key: Question}'''
        return requirement_key_dictionary

    async def update_prompt_requirement_questions(self, function_list, prompt):
        dict = await self.create_requirement_key_dictionary(function_list)
        prompt_with_date = f"Today is {date.today()}. {prompt}"
        if not dict:
            return prompt_with_date

        dict_explain = "Following dictionary is for you to use which question you should ask if required parameters of the function is not present. Ask the exact question with exact words in the dictionary to find the function's required parameter"    
        updated_prompt = f"{prompt_with_date} {dict_explain} {dict}"
        return updated_prompt
