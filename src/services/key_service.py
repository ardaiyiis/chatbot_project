from models import FunctionKey, Key

def generate_key_properties(function_id, session):
    # Query the database to fetch keys associated with the function
    keys = session.query(Key).join(FunctionKey).filter(FunctionKey.function_id == function_id).all()

    properties = {}
    for key in keys:
        property_name = key.name
        property_type = key.type
        property_description = key.description

        properties[property_name] = {
            "type": property_type,
            "description": property_description
        }

    return properties