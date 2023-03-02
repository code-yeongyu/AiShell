import os
from typing import Final, Optional

from revChatGPT.V3 import Chatbot

from aishell.exceptions import UnauthorizedAccessError
from aishell.utils import make_executable_command

from .query_client import QueryClient


class OfficialChatGPTClient(QueryClient):
    openai_api_key: str

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
    ):
        super().__init__()
        OPENAI_API_KEY: Final[Optional[str]] = os.environ.get('OPENAI_API_KEY', openai_api_key)
        if OPENAI_API_KEY is None:
            raise UnauthorizedAccessError('OPENAI_API_KEY should not be none')

        self.openai_api_key = OPENAI_API_KEY

    def _construct_prompt(self, text: str) -> str:
        return f'''You are now a translater from human language to {os.uname()[0]} shell command.
        No explanation required, respond with only the raw shell command.
        What should I type to shell for: {text}, in one line.'''

    def query(self, prompt: str) -> str:
        prompt = self._construct_prompt(prompt)

        chatbot = Chatbot(api_key=self.openai_api_key)
        response_text = chatbot.ask(prompt)

        return make_executable_command(response_text)
