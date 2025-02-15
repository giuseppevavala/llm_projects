# class ClaudeRequestHandler(RequestHandler):
#     def prepare_request(self, messages: List[Dict[str, str]], **kwargs) -> Dict:
#         return {
#             "messages": messages,
#             **kwargs
#         }
    
#     def process_response(self, response: requests.Response) -> str:
#         return response.json()["content"][0]["text"]

# class OllamaRequestHandler(RequestHandler):
#     def prepare_request(self, messages: List[Dict[str, str]], **kwargs) -> Dict:
#         prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
#         return {"prompt": prompt, **kwargs}
    
#     def process_response(self, response: requests.Response) -> str:
#         response_text = ""
#         for line in response.text.strip().split("\n"):
#             event = json.loads(line)
#             if "response" in event:
#                 response_text += event["response"]
#         return response_text




# class ClaudeModel(LanguageModel):
#     def __init__(self, model: str = "claude-3-sonnet-20240229"):
#         super().__init__()
#         self.model = model
#         self.api_url = "https://api.anthropic.com/v1/messages"
    
#     def initialize_handler(self):
#         self.request_handler = ClaudeRequestHandler()
    
#     def _make_request(self, data: Dict) -> requests.Response:
#         headers = {
#             "x-api-key": self.config.get('claude_api_key'),
#             "anthropic-version": "2023-06-01",
#             "content-type": "application/json"
#         }
#         data["model"] = self.model
#         return requests.post(self.api_url, headers=headers, json=data)

# class OllamaModel(LanguageModel):
#     def __init__(self, model: str = "llama2"):
#         super().__init__()
#         self.model = model
#         self.api_url = f"{self.config.get('ollama_url')}/api/generate"
    
#     def initialize_handler(self):
#         self.request_handler = OllamaRequestHandler()
    
#     def _make_request(self, data: Dict) -> requests.Response:
#         data["model"] = self.model
#         return requests.post(self.api_url, json=data)

