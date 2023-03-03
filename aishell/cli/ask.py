import os

import typer
from rich.console import Console

from aishell.models.language_model import LanguageModel
from aishell.query_clients import GPT3Client, OfficialChatGPTClient, QueryClient, ReverseEngineeredChatGPTClient
from aishell.utils import AiShellConfigManager

from . import cli_app
from .config_aishell import config_aishell


@cli_app.command()
def ask(question: str, language_model: LanguageModel = LanguageModel.REVERSE_ENGINEERED_CHATGPT):
    is_config_file_available = AiShellConfigManager.is_config_file_available(AiShellConfigManager.DEFAULT_CONFIG_PATH)
    config_manager: AiShellConfigManager
    if is_config_file_available:
        config_manager = AiShellConfigManager(load_config=True)
    else:
        config_manager = config_aishell()
    config_manager.config_model.language_model = language_model
    configured_language_model = config_manager.config_model.language_model

    query_client: QueryClient
    if configured_language_model == LanguageModel.REVERSE_ENGINEERED_CHATGPT:
        query_client = ReverseEngineeredChatGPTClient(config=config_manager.config_model.chatgpt_config)
    elif configured_language_model == LanguageModel.GPT3:
        query_client = GPT3Client()
    elif configured_language_model == LanguageModel.OFFICIAL_CHATGPT:
        query_client = OfficialChatGPTClient()
    else:
        raise NotImplementedError(f'Language model {configured_language_model} is not implemented yet.')

    query_client.query(question)

    console = Console()
    with console.status(f'''
[green] AiShell is thinking of `{question}` ...[/green]

[dim]AiShell is not responsible for any damage caused by the command executed by the user.[/dim]'''.strip()):
        response = query_client.query(question)
    console.print(f'AiShell: {response}\n')

    will_execute = typer.confirm('Execute this command?')

    if will_execute:
        os.system(response)
