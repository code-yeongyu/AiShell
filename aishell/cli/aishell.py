import os
import time
from typing import Optional

import typer
from rich.console import Console
from ygka.models import LanguageModel
from ygka.query_clients import QueryClientFactory
from ygka.utils import YGKAConfigManager

from aishell.utils import construct_prompt

from .cli_app import cli_app
from .config_aishell import config_aishell


@cli_app.command()
def aishell_command(question: str, language_model: Optional[LanguageModel] = None):
    config_manager = _get_config_manager()
    config_manager.config_model.language_model = language_model or config_manager.config_model.language_model

    query_client = QueryClientFactory(config_model=config_manager.config_model).create()

    console = Console()

    with console.status(f'''
[green] AiShell is thinking of `{question}` ...[/green]

[dim]AiShell is not responsible for any damage caused by the command executed by the user.[/dim]'''[1:]):
        start_time = time.time()
        response = query_client.query(construct_prompt(question))
        end_time = time.time()

    execution_time = end_time - start_time
    console.print(f'AiShell: {response}\n\n[dim]Took {execution_time:.2f} seconds to think the command.[/dim]')

    will_execute = typer.confirm('Execute this command?')
    if will_execute:
        os.system(response)


def _get_config_manager():
    is_config_file_available = YGKAConfigManager.is_config_file_available(YGKAConfigManager.DEFAULT_CONFIG_PATH)
    if is_config_file_available:
        return YGKAConfigManager(load_config=True)
    else:
        return config_aishell()
