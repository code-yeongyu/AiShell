import os
import time
from typing import Optional

import rich
import typer
from rich.console import Console

from aishell.models import AiShellConfigModel
from aishell.models.language_model import LanguageModel
from aishell.query_clients import GPT3Client, OfficialChatGPTClient, ReverseEngineeredChatGPTClient
from aishell.utils import AiShellConfigManager

from .cli_app import cli_app
from .config_aishell import config_aishell


@cli_app.command()
def aishell_command(question: str, language_model: Optional[LanguageModel] = None):
    config_manager = _get_config_manager()
    config_manager.config_model.language_model = language_model or config_manager.config_model.language_model

    query_client = _get_query_client(
        language_model=config_manager.config_model.language_model,
        config_model=config_manager.config_model,
    )

    console = Console()

    try:
        with console.status(f'''
[green] AiShell is thinking of `{question}` ...[/green]

[dim]AiShell is not responsible for any damage caused by the command executed by the user.[/dim]'''[1:]):
            start_time = time.time()
            response = query_client.query(question)
            end_time = time.time()

        execution_time = end_time - start_time
        console.print(f'AiShell: {response}\n\n[dim]Took {execution_time:.2f} seconds to think the command.[/dim]')

        will_execute = typer.confirm('Execute this command?')
        if will_execute:
            os.system(response)
    except KeyError:
        rich.print('It looks like the `session_token` is expired. Please reconfigure AiShell.')
        typer.confirm('Reconfigure AiShell?', abort=True)
        config_aishell()
        aishell_command(question=question, language_model=language_model)
        typer.Exit()


def _get_config_manager():
    is_config_file_available = AiShellConfigManager.is_config_file_available(AiShellConfigManager.DEFAULT_CONFIG_PATH)
    if is_config_file_available:
        return AiShellConfigManager(load_config=True)
    else:
        return config_aishell()


def _get_query_client(language_model: LanguageModel, config_model: AiShellConfigModel):
    if language_model == LanguageModel.REVERSE_ENGINEERED_CHATGPT:
        return ReverseEngineeredChatGPTClient(config=config_model.chatgpt_config)

    if not config_model.openai_api_key:
        raise RuntimeError('OpenAI API key is not provided. Please provide it in the config file.')

    if language_model == LanguageModel.GPT3:
        return GPT3Client(openai_api_key=config_model.openai_api_key)
    if language_model == LanguageModel.OFFICIAL_CHATGPT:
        return OfficialChatGPTClient(openai_api_key=config_model.openai_api_key)
    raise NotImplementedError(f'Language model {language_model} is not implemented yet.')
