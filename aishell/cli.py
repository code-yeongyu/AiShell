import os
import webbrowser

import typer
from rich.console import Console
from yt_dlp.cookies import SUPPORTED_BROWSERS

from aishell.adapters.openai_chatgpt_adapter import OpenAIChatGPTAdapter
from aishell.exceptions import UnauthorizedAccessError
from aishell.models.language_model import LanguageModel
from aishell.query_clients import GPT3Client, OfficialChatGPTClient, QueryClient, ReverseEngineeredChatGPTClient

cli_app = typer.Typer()


def _open_chatgpt_browser():
    CHATGPT_LOGIN_URL = 'https://chat.openai.com/auth/login?next=/chat'
    webbrowser.open(CHATGPT_LOGIN_URL)


@cli_app.command()
def ask(question: str, language_model: LanguageModel = LanguageModel.REVERSE_ENGINEERED_CHATGPT):
    query_client: QueryClient
    if language_model == LanguageModel.GPT3:
        query_client = GPT3Client()
    elif language_model == LanguageModel.OFFICIAL_CHATGPT:
        query_client = OfficialChatGPTClient()
    elif language_model == LanguageModel.REVERSE_ENGINEERED_CHATGPT:
        try:
            query_client = ReverseEngineeredChatGPTClient()
        except UnauthorizedAccessError:
            print('You are not logged in to OpenAI, attempting to log you in...')
            _open_chatgpt_browser()
            BROWSER_NAME = typer.prompt(f'Which browser did you use to log in? [{SUPPORTED_BROWSERS}]')
            adapter = OpenAIChatGPTAdapter(BROWSER_NAME)
            session_token = adapter.get_openai_session_token()
            query_client = ReverseEngineeredChatGPTClient(session_token=session_token)

    query_client.query(question)

    console = Console()
    with console.status(
            f'''
[green] AiShell is thinking of `{question}` ...[/green]

[italic]AiShell is not responsible for any damage caused by the command executed by the user.[/italic]'''.strip(), ):
        response = query_client.query(question)
    console.print(f'[italic]ai$hell: {response}\n')

    will_execute = typer.confirm('Execute this command?')

    if will_execute:
        os.system(response)
