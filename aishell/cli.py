import os

import typer
from rich.console import Console

from aishell.query_clients import ChatGPTClient, GPT3Client, QueryClient

cli_app = typer.Typer()


@cli_app.command()
def ask(question: str, use_chatgpt: bool = False):
    query_client: QueryClient
    if use_chatgpt:
        query_client = ChatGPTClient()
    else:
        query_client = GPT3Client()

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
