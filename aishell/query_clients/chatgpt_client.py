import os
from typing import Optional

from revChatGPT.V1 import Chatbot

from aishell.utils import make_executable_command

from .query_client import QueryClient


class ChatGPTClient(QueryClient):
    access_key: str

    def __init__(
        self,
        chatgpt_access_key: Optional[str] = None,
    ):
        super().__init__()
        CHATGPT_ACCESS_KEY = os.environ.get('CHATGPT_ACCESS_KEY')

        if chatgpt_access_key is not None:
            self.access_key = chatgpt_access_key
        elif CHATGPT_ACCESS_KEY is not None:
            self.access_key = CHATGPT_ACCESS_KEY
        else:
            raise Exception('access_key should not be none')

    def _construct_prompt(self, text: str) -> str:
        return f'''You are now a translater from human language to {os.uname()[0]} shell command.
        No explanation required, respond with only the raw shell command.
        What should I type to shell for: {text}, in one line.'''

    def query(self, prompt: str) -> str:
        prompt = self._construct_prompt(prompt)
        chatbot = Chatbot(config={'access_token': self.access_key})

        response_text = ''
        for data in chatbot.ask(prompt):
            response_text = data['message']

        response_text = make_executable_command(response_text)

        return response_text
