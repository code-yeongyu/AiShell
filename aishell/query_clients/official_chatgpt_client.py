import os
from typing import Optional

from revChatGPT.V3 import Chatbot

from aishell.exceptions import UnauthorizedAccessError
from aishell.utils import make_executable_command

from .query_client import QueryClient


class OfficialChatGPTClient(QueryClient):

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
    ):
        super().__init__()
        OPENAI_API_KEY: Optional[str] = os.environ.get('OPENAI_API_KEY', openai_api_key)
        if OPENAI_API_KEY is None:
            raise UnauthorizedAccessError('OPENAI_API_KEY should not be none')

        self.OPENAI_API_KEY = OPENAI_API_KEY

    def query(self, prompt: str) -> str:
        chatbot = Chatbot(api_key=self.OPENAI_API_KEY)

        prompt = self._construct_prompt(prompt)
        response_text = chatbot.ask(prompt)
        executable_command = make_executable_command(response_text)
        return executable_command

    def _construct_prompt(self, text: str) -> str:
        return f'''You are now a translater from human language to {os.uname()[0]} shell command.
        No explanation required, respond with only the raw shell command.
        What should I type to shell for: {text}, in one line.'''
