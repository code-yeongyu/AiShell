import os
import sys

import rich
import typer
from rich.console import Console
from yt_dlp.cookies import SUPPORTED_BROWSERS

from aishell.adapters.openai_cookie_adapter import OpenAICookieAdapter
from aishell.models import RevChatGPTChatbotConfigModel
from aishell.models.aishell_config_model import AiShellConfigModel
from aishell.models.language_model import LanguageModel
from aishell.query_clients import GPT3Client, OfficialChatGPTClient, QueryClient, ReverseEngineeredChatGPTClient
from aishell.utils import AiShellConfigManager

cli_app = typer.Typer()


def config_aishell():
    rich.print('''Hi! 🙌 I am [bold blue]AiShell[/bold blue], [yellow]your powerful terminal assistant[/yellow] 🔥
I am here to assist you with configuring AiShell. 💪

Please make sure that you have logged into chat.openai.com on your browser before we continue. 🗝️

''')
    typer.confirm('Are you ready to proceed? 🚀', abort=True)

    rich.print(f'''Which browser did you use to log in to chat.openai.com?

We support the following browsers: [{SUPPORTED_BROWSERS}]''')
    browser_name = typer.prompt('Please enter your choice here: ')
    if browser_name not in SUPPORTED_BROWSERS:
        rich.print(f'Browser {browser_name} is not supported. Supported browsers are: {SUPPORTED_BROWSERS}')
        sys.exit(1)

    adapter = OpenAICookieAdapter(browser_name)
    session_token = adapter.get_openai_session_token()
    if not session_token:
        rich.print('Failed to get session token. 😓 Can you check if you are logged in to https://chat.openai.com?')
        sys.exit(1)

    is_paid = typer.confirm("It's my last question! 🤩 Are you a PLUS user?")

    chatgpt_config = RevChatGPTChatbotConfigModel(session_token=session_token, paid=is_paid)
    aishell_config = AiShellConfigModel(chatgpt_config=chatgpt_config)
    config_manager = AiShellConfigManager(config_model=aishell_config)
    config_manager.save_config()

    rich.print(f'''[green bold]Excellent![/green bold] You are now ready to use [bold blue]AiShell[/bold blue] 🚀

Enjoy your AI powered terminal assistant! 🎉

[dim]To check your settings file, it's at: {config_manager.config_path}[/dim]

''')
    return config_manager


@cli_app.command()
def ask(question: str, language_model: LanguageModel = LanguageModel.REVERSE_ENGINEERED_CHATGPT):
    is_config_file_available = AiShellConfigManager.is_config_file_available(AiShellConfigManager.DEFAULT_CONFIG_PATH)
    config_manager: AiShellConfigManager
    if is_config_file_available:
        config_manager = AiShellConfigManager(load_config=True)
    else:
        config_manager = config_aishell()

    query_client: QueryClient
    if language_model == LanguageModel.REVERSE_ENGINEERED_CHATGPT:
        query_client = ReverseEngineeredChatGPTClient(config=config_manager.config_model.chatgpt_config)
    elif language_model == LanguageModel.GPT3:
        query_client = GPT3Client()
    elif language_model == LanguageModel.OFFICIAL_CHATGPT:
        query_client = OfficialChatGPTClient()

    query_client.query(question)

    console = Console()
    with console.status(
            f'''
[green] AiShell is thinking of `{question}` ...[/green]

[dim]AiShell is not responsible for any damage caused by the command executed by the user.[/dim]'''.strip(), ):
        response = query_client.query(question)
    console.print(f'AiShell: {response}\n')

    will_execute = typer.confirm('Execute this command?')

    if will_execute:
        os.system(response)
