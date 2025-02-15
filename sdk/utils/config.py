import os

from dotenv import load_dotenv

class Configuration:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        load_dotenv()

        self.config = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
        } 
    
    def get(self, key: str) -> str:
        return self.config.get(key)