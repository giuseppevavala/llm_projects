import requests

from .base import LanguageModel, RequestHandler, ModelName
from typing import List, Dict

class OpenAiModelName(ModelName):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"


class OpenAIRequestHandler(RequestHandler):
    def prepare_request(self, messages: List[Dict[str, str]], **kwargs) -> Dict:
        return {"messages": messages, **kwargs}

    def process_response(self, response: requests.Response) -> str:
        json_response = response.json()

        if "error" in json_response:
            raise ValueError(json_response["error"]["message"])

        return json_response["choices"][0]["message"]["content"]


class OpenAIModel(LanguageModel):
    def __init__(self, modelName: ModelName):
        super().__init__()
        self.model = modelName
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def initialize_handler(self):
        self.request_handler = OpenAIRequestHandler()

    def _make_request(self, data: Dict) -> requests.Response:
        headers = {
            "Authorization": f"Bearer {self.config.get('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        }
        data["model"] = self.model.value
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()

        return response
