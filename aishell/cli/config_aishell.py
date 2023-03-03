import sys

import rich
import typer
from yt_dlp.cookies import SUPPORTED_BROWSERS

from aishell.adapters.openai_cookie_adapter import OpenAICookieAdapter
from aishell.models import RevChatGPTChatbotConfigModel
from aishell.models.aishell_config_model import AiShellConfigModel
from aishell.utils import AiShellConfigManager


def config_aishell():
    rich.print('''
Hi! 🙌 I am [bold blue]AiShell[/bold blue], [yellow]your powerful terminal assistant[/yellow] 🔥
I am here to assist you with configuring AiShell. 💪

Please make sure that you have logged into chat.openai.com on your browser before we continue. 🗝️

'''[1:])
    typer.confirm('Are you ready to proceed? 🚀', abort=True)

    rich.print(f'''
Which browser did you use to log in to chat.openai.com?

We support the following browsers: [{SUPPORTED_BROWSERS}]'''[1:])
    browser_name = typer.prompt('Please enter your choice here: ')
    if browser_name not in SUPPORTED_BROWSERS:
        rich.print(f'Browser {browser_name} is not supported. Supported browsers are: {SUPPORTED_BROWSERS}')
        sys.exit(1)

    adapter = OpenAICookieAdapter(browser_name)
    session_token = adapter.get_openai_session_token()
    if not session_token:
        rich.print('Failed to get session token. 😓 Can you check if you are logged in to https://chat.openai.com?')
        sys.exit(1)

    config_manager = save_config(session_token)

    rich.print(f'''
[green bold]Excellent![/green bold] You are now ready to use [bold blue]AiShell[/bold blue] 🚀

Enjoy your AI powered terminal assistant! 🎉

[dim]To check your settings file, it's at: {config_manager.config_path}[/dim]

'''[1:])
    return config_manager


def save_config(session_token: str):
    is_config_file_available = AiShellConfigManager.is_config_file_available(AiShellConfigManager.DEFAULT_CONFIG_PATH)
    if is_config_file_available:
        config_manager = AiShellConfigManager(load_config=True)
        is_chatgpt_config_available = config_manager.config_model.chatgpt_config is not None
        if is_chatgpt_config_available:
            assert config_manager.config_model.chatgpt_config  # for type hinting
            config_manager.config_model.chatgpt_config.session_token = session_token
        else:
            config_manager.config_model.chatgpt_config = RevChatGPTChatbotConfigModel(session_token=session_token)
    else:
        chatgpt_config = RevChatGPTChatbotConfigModel(session_token=session_token)
        aishell_config = AiShellConfigModel(chatgpt_config=chatgpt_config)
        config_manager = AiShellConfigManager(config_model=aishell_config)

    config_manager.save_config()
    return config_manager
