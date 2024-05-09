class FunctionService:

    def get_function_list(self, function_list):
        functions = function_list
        function_data_list = []

        for function in functions:
            if function.is_active:
                required_keys = [function_key.key.name for function_key in function.keys if function_key.is_required]
                properties = {}  # Initialize the properties dictionary

                # Retrieve key properties
                for function_key in function.keys:
                    key = function_key.key
                    property_name = key.name
                    property_type = key.type
                    property_description = key.description

                    properties[property_name] = {
                        "type": property_type,
                        "description": property_description
                    }

                function_data = {
                    "name": function.name,
                    "description": function.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,  # Use the properties dictionary
                        "required": required_keys
                    },
                }
                function_data_list.append(function_data)

        return function_data_list

