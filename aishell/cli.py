import os

import typer
from rich.console import Console

from aishell.models.language_model import LanguageModel
from aishell.query_clients import GPT3Client, OfficialChatGPTClient, QueryClient, ReverseEngineeredChatGPTClient

cli_app = typer.Typer()


@cli_app.command()
def ask(question: str, language_model: LanguageModel = LanguageModel.OFFICIAL_CHATGPT):
    query_client: QueryClient
    if language_model == LanguageModel.GPT3:
        query_client = GPT3Client()
    elif language_model == LanguageModel.OFFICIAL_CHATGPT:
        query_client = OfficialChatGPTClient()
    elif language_model == LanguageModel.REVERSE_ENGINEERED_CHATGPT:
        query_client = ReverseEngineeredChatGPTClient()

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
