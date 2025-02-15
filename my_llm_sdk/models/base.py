import requests

from abc import ABC, abstractmethod
from typing import List, Dict
from enum import Enum

from ..utils.decorators import log_execution_time
from ..utils.config import Configuration

class ModelName(Enum):
    pass


class RequestHandler(ABC):
    @abstractmethod
    def prepare_request(self, messages: List[Dict[str, str]], **kwargs) -> Dict:
        pass

    @abstractmethod
    def process_response(self, response: requests.Response) -> str:
        pass


class LanguageModel(ABC):
    def __init__(self):
        self.config = Configuration()
        self.request_handler: RequestHandler = None

    @abstractmethod
    def initialize_handler(self):
        pass

    @log_execution_time
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        if not self.request_handler:
            self.initialize_handler()

        data = self.request_handler.prepare_request(messages, **kwargs)
        response = self._make_request(data)
        return self.request_handler.process_response(response)

    @abstractmethod
    def _make_request(self, data: Dict) -> requests.Response:
        pass
