from enum import Enum

from .open_ai import OpenAiModelName, OpenAIModel
from .ollama import OllamaModelName, OllamaModel
from .grammar import GrammarModelName, GrammarModel
from .base import LanguageModel
from .base import ModelName

class ModelFactory:
    @staticmethod
    def create_model(model_name: ModelName) -> LanguageModel:
        if isinstance(model_name, OpenAiModelName):
            return OpenAIModel(model_name)
        elif isinstance(model_name, OllamaModelName):
            return OllamaModel(model_name)
        elif isinstance(model_name, GrammarModelName):
            return GrammarModel(model_name)
        else:
            raise ValueError(f"Model {model_name} not supported")