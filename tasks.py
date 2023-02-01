import shutil

import toml
from colorama import Fore
from colorama import init as init_colorama
from invoke import Context, task

import monkey_patch_invoke as _    # noqa


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        project_name = get_pep8_compliant_name(data['tool']['poetry']['name'])
        return project_name


@task
def run(context: Context):
    context.run(f'python {get_project_path()}/main.py', pty=True)


@task
def test(context: Context):
    context.run('pytest . --cov=. --cov-report=xml', pty=True)


@task
def format_code(context: Context) -> None:
    init_colorama()

    print(f'{Fore.MAGENTA}==========Remove unused imports with `autoflake`=========={Fore.RESET}')
    context.run(f'pautoflake {get_project_path()}', pty=True)

    print(f'{Fore.MAGENTA}==========Sort imports with `isort`=========={Fore.RESET}')
    context.run(f'isort {get_project_path()}', pty=True)

    print(f'{Fore.MAGENTA}==========Unifying quotes with `unify`=========={Fore.RESET}')
    context.run(f'unify --in-place -r {get_project_path()}')

    print(f'{Fore.MAGENTA}==========Format code with `yapf`=========={Fore.RESET}')
    context.run(f'yapf --in-place --recursive --parallel {get_project_path()}', pty=True)


@task
def check(context: Context):
    check_code_style(context)
    check_types(context)


@task
def check_code_style(context: Context):
    init_colorama()

    print(f'{Fore.MAGENTA}==========Check Code Styles with `autoflake`=========={Fore.GREEN}')
    context.run(f'pautoflake {get_project_path()} --check', pty=True)

    print(f'{Fore.MAGENTA}==========Check Code Styles with `isort`=========={Fore.GREEN}')
    context.run(f'isort {get_project_path()} --check --diff', pty=True)
    print(f'{Fore.GREEN}isort: Success{Fore.RESET}')

    print(f'{Fore.MAGENTA}==========Check Code Styles with `pylint`=========={Fore.GREEN}')
    context.run(f'pylint {get_project_path()}', pty=True)

    print(f'{Fore.MAGENTA}==========Check Code Styles with `yapf`=========={Fore.RESET}')
    context.run(f'yapf --diff --recursive --parallel {get_project_path()}', pty=True)
    print(f'{Fore.GREEN}yapf: Success{Fore.RESET}')


@task
def check_types(context: Context):
    """Check types with `pyright` and `mypy`."""
    init_colorama()

    print(f'{Fore.CYAN}==========Check typings with `pyright`=========={Fore.RESET}')
    context.run(f'pyright {get_project_path()}', pty=True)

    print(f'\n{Fore.CYAN}==========Check typings with `mypy`=========={Fore.RESET}')
    context.run(f'mypy {get_project_path()}', pty=True)


@task
def rename_project(_context: Context, project_name: str):
    # Get the current project path
    current_project_path = get_project_path()

    # Rename the directory
    shutil.move(get_pep8_compliant_name(current_project_path), get_pep8_compliant_name(project_name))

    # Update the project name in pyproject.toml
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = toml.load(file)

    data['tool']['poetry']['name'] = project_name

    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        toml.dump(data, file)
