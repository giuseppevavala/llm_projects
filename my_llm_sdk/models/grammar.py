from .base import LanguageModel, RequestHandler, ModelName
import spacy
import nltk
from textblob import TextBlob
from typing import List, Dict
import requests

class GrammarModelName(ModelName):
    SPACY = "spacy"
    NLTK = "nltk"
    TEXTBLOB = "textblob"

class GrammarRequestHandler(RequestHandler):
    def prepare_request(self, messages: List[Dict[str, str]], **kwargs) -> Dict:
        # Per i modelli di grammatica, prendiamo solo l'ultimo messaggio
        last_message = messages[-1]["content"] if messages else ""
        return {
            "text": last_message,
            **kwargs
        }

    def process_response(self, response: requests.Response) -> str:
        return response.json()["analysis"]

class GrammarModel(LanguageModel):
    def __init__(self, modelName: ModelName):
        super().__init__()
        self.model = modelName
        self._initialize_models()

    def _initialize_models(self):
        if self.model == GrammarModelName.SPACY:
            self.nlp = spacy.load("en_core_web_sm")
        elif self.model == GrammarModelName.NLTK:
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')
        # TextBlob non richiede inizializzazione speciale

    def initialize_handler(self):
        self.request_handler = GrammarRequestHandler()

    def _make_request(self, data: Dict) -> requests.Response:
        text = data["text"]
        analysis = ""

        if self.model == GrammarModelName.SPACY:
            doc = self.nlp(text)
            analysis = {
                "tokens": [token.text for token in doc],
                "pos_tags": [(token.text, token.pos_) for token in doc]
            }
        elif self.model == GrammarModelName.NLTK:
            tokens = nltk.word_tokenize(text)
            analysis = {
                "tokens": tokens,
                "pos_tags": nltk.pos_tag(tokens)
            }
        elif self.model == GrammarModelName.TEXTBLOB:
            blob = TextBlob(text)
            analysis = {
                "tokens": list(blob.words),
                "pos_tags": blob.tags
            }

        # Simuliamo una response di requests per mantenere la compatibilità
        class MockResponse:
            def __init__(self, data):
                self._data = data
            
            def json(self):
                return {"analysis": self._data}
            
            def raise_for_status(self):
                pass

        return MockResponse(analysis) 