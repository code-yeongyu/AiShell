import sys

import rich
import typer
from revChatGPTAuth import SupportedBrowser
from ygka.cli.config_ygka import save_config


def config_aishell():
    SUPPORTED_BROWSERS = [browser.value for browser in SupportedBrowser]
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

    config_manager = save_config(browser_name=browser_name)

    rich.print(f'''
[green bold]Excellent![/green bold] You are now ready to use [bold blue]AiShell[/bold blue] 🚀

Enjoy your AI powered terminal assistant! 🎉

[dim]To check your settings file, it's at: {config_manager.config_path}[/dim]

'''[1:])
    return config_manager
