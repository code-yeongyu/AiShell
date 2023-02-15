import os
from typing import Optional

from revChatGPT.Official import Chatbot
from utils import make_executable_command

from .query_client import QueryClient


class ChatGPTClient(QueryClient):

    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')
        if api_key is None or OPEN_API_KEY is None:
            raise Exception('api_key should not be none')
        self.API_KEY = api_key or OPEN_API_KEY

    def _construct_prompt(self, text: str) -> str:
        return f'''You are now a translater from human language to {os.uname()[0]} shell command.
        No explanation required, respond with only the raw shell command.
        What should I type to shell for: {text}, in one line.'''

    def query(self, prompt: str) -> str:
        prompt = self._construct_prompt(prompt)
        chatbot = Chatbot(api_key=self.API_KEY)
        response_text: str = chatbot.ask(prompt)['choices'][0]['text']
        return make_executable_command(response_text)
