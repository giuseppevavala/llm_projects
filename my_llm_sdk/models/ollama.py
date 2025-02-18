from .base import LanguageModel, RequestHandler, ModelName
import requests
from typing import List, Dict

class OllamaModelName(ModelName):
    LLAMA_3_2 = "llama3.2"

class OllamaRequestHandler(RequestHandler):
    def prepare_request(self, messages: List[Dict[str, str]], **kwargs) -> Dict:
        # Ollama usa un formato leggermente diverso per i messaggi
        return {
            "messages": messages,
            "stream": False,
            **kwargs
        }

    def process_response(self, response: requests.Response) -> str:
        json_response = response.json()
        
        if "error" in json_response:
            raise ValueError(json_response["error"])
            
        return json_response["message"]["content"]

class OllamaModel(LanguageModel):
    def __init__(self, modelName: ModelName):
        super().__init__()
        self.model = modelName
        # Ollama viene eseguito localmente sulla porta 11434 di default
        self.api_url = "http://localhost:11434/api/chat"

    def initialize_handler(self):
        self.request_handler = OllamaRequestHandler()

    def _make_request(self, data: Dict) -> requests.Response:
        headers = {
            "Content-Type": "application/json",
        }
        data["model"] = self.model.value
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()

        return response