from typing import NamedTuple, Dict

class Config(NamedTuple):
    openai_api_key: str
    gupshup_api_key: str
    model_name: str
    temperature: float  # Assuming temperature is a float, update accordingly
    promptBase: str
    functions: list