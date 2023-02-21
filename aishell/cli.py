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
    with console.status(f'[green] Asking `{question}` ...'):
        response = query_client.query(question)
    console.print(f'[italic]ai$hell: {response}\n')

    os.system(response)
