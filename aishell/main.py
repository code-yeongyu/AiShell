#!/usr/bin/env python

from revChatGPT.Official import Chatbot

import os
import typer

API_KEY = os.environ.get('OPENAI_API_KEY') or ''


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
    chatbot = Chatbot(api_key=API_KEY)
    response_text: str = chatbot.ask(text)['choices'][0]['text']
    return make_executable_command(response_text)


def get_os() -> str:
    return os.uname()[0]


def make_prompt(requirements: str) -> str:
    return f'''You are now a translater from human language to {get_os} shell command.
    No explanation required, respond with only the raw shell command.
    What should I type to shell for: {requirements}, in one line.'''


app = typer.Typer()


@app.command()
def ask(text: str):
    question = make_prompt(text)
    response = ask_chatgpt(question)
    typer.echo(f'\033[3mexecuted: {response}\033[0m')
    os.system(response)


if __name__ == '__main__':
    app()
