#!/usr/bin/env python

import os
from typing import List, Optional, cast

import openai
import typer
from pydantic import BaseModel
from revChatGPT.Official import Chatbot

API_KEY = os.environ.get('OPENAI_API_KEY') or ''


class OpenAIResponseModel(BaseModel):

    class Choice(BaseModel):
        finish_reason: str
        index: int
        logprobs: Optional[None]
        text: Optional[str]

    class Usage(BaseModel):
        completion_tokens: int
        prompt_tokens: int
        total_tokens: int

    choices: Optional[List[Choice]]
    created: int
    id: str
    model: str
    object: str
    usage: Usage


def get_os() -> str:
    return os.uname()[0]


def make_executable_command(command: str) -> str:
    # starting '\n' or trailing '\n' should be replaced as ''
    # starting ' ' or trailing ' ' should be replaced as ''
    if command.startswith('\n'):
        command = command[1:]
    if command.endswith('\n'):
        command = command[:-1]
    if command.startswith('`'):
        command = command[1:]
    if command.endswith('`'):
        command = command[:-1]
    command = command.strip()
    command = command.split('User: ')[0]
    return command


def ask_chatgpt(text: str) -> str:

    def _construct_prompt(requirements: str) -> str:
        return f'''You are now a translater from human language to {get_os()} shell command.
        No explanation required, respond with only the raw shell command.
        What should I type to shell for: {requirements}, in one line.'''

    prompt = _construct_prompt(text)
    chatbot = Chatbot(api_key=API_KEY)
    response_text: str = chatbot.ask(prompt)['choices'][0]['text']
    return make_executable_command(response_text)


def ask_gpt3(text: str) -> str:

    def _construct_prompt(text: str) -> str:
        return f'''User: You are now a translater from human language to {get_os()} shell command.
        No explanation required, respond with only the raw shell command.
        What should I type to shell for: {text}, in one line.

        You: '''

    prompt = _construct_prompt(text)

    completion: OpenAIResponseModel = cast(
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
    response_text: str = completion.choices[0].text
    return make_executable_command(response_text)


app = typer.Typer()


@app.command()
def ask(question: str, use_chatgpt: bool = False):
    if use_chatgpt:
        response = ask_chatgpt(question)
    else:
        response = ask_gpt3(question)
    typer.echo(f'\033[3mexecuting: {response}\033[0m')
    os.system(response)


if __name__ == '__main__':
    app()
