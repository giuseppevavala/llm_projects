from enum import Enum

from .open_ai import OpenAiModelName, OpenAIModel
from .base import LanguageModel
from .base import ModelName

# class ModelFamily(Enum):
#     OPENAI = "openai"
#     CLAUDE = "claude"
#     OLLAMA = "ollama"


class ModelFactory:
    @staticmethod
    def create_model(model_name: ModelName) -> LanguageModel:
        print (model_name)
        print (isinstance(model_name, OpenAiModelName) )
        if isinstance(model_name, OpenAiModelName):
            return OpenAIModel(model_name)
        else:
            raise ValueError(f"Model {model_name} not supported")