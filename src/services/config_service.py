import json
import os
from models.configs import Config
class ConfigService:
    def __init__(self):
        cfg = self.get_config()
        self.config:Config = Config(**cfg)

    def get_config(self):
        path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'config.json')
        with open(path_to_json, 'r', encoding='utf-8') as f:
            file = json.load(f)
            return file

   