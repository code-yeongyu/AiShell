import os
from typing import Final, cast

import openai

from aishell.models import OpenAIResponseModel
from aishell.utils import make_executable_command

from .query_client import QueryClient


class GPT3Client(QueryClient):

    def __init__(
        self,
        openai_api_key: str,
    ):
        openai.api_key = openai_api_key

    def query(self, prompt: str) -> str:
        prompt = self._construct_prompt(prompt)
        completion: Final[OpenAIResponseModel] = cast(
            OpenAIResponseModel,
            openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                temperature=0.5,
                max_tokens=4000 - len(prompt),
                stop=['\n\n\n'],
            ),
        )
        if not completion.choices or len(completion.choices) == 0 or not completion.choices[0].text:
            raise RuntimeError('No response from OpenAI')
        response_text: Final[str] = completion.choices[0].text
        return make_executable_command(response_text)

    def _construct_prompt(self, text: str) -> str:
        return f'''
User: You are now a translater from human language to {os.uname()[0]} shell command.
No explanation required, respond with only the raw shell command.
What should I type to shell for: {text}, in one line.

You: '''[1:]
