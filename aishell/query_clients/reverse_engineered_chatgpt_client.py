import os
from typing import Optional, cast

from revChatGPT.V1 import Chatbot

from aishell.exceptions import UnauthorizedAccessError
from aishell.utils import make_executable_command

from .query_client import QueryClient


class ReverseEngineeredChatGPTClient(QueryClient):
    config: dict[str, str] = {}

    def __init__(
        self,
        access_token: Optional[str] = None,
        session_token: Optional[str] = None,
    ):
        CHATGPT_ACCESS_TOKEN = os.environ.get('CHATGPT_ACCESS_TOKEN', access_token)
        CHATGPT_SESSION_TOKEN = os.environ.get('CHATGPT_SESSION_TOKEN', session_token)
        if CHATGPT_ACCESS_TOKEN is not None:
            self.config['access_token'] = CHATGPT_ACCESS_TOKEN
        elif CHATGPT_SESSION_TOKEN is not None:
            self.config['session_token'] = CHATGPT_SESSION_TOKEN
        else:
            raise UnauthorizedAccessError('No access token or session token provided.')

    def _construct_prompt(self, text: str) -> str:
        return f'''You are now a translater from human language to {os.uname()[0]} shell command.
        No explanation required, respond with only the raw shell command.
        What should I type to shell for: {text}, in one line.'''

    def query(self, prompt: str) -> str:
        prompt = self._construct_prompt(prompt)
        chatbot = Chatbot(config=self.config)

        response_text = ''
        for data in chatbot.ask(prompt):
            response_text = data['message']

        response_text = make_executable_command(cast(str, response_text))

        return response_text
