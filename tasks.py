# type: ignore
import shutil
import subprocess

import toml
from invoke import Context, task
from rich.console import Console

import monkey_patch_invoke as _  # noqa: F401

console = Console()


def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')


def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        project_name = get_pep8_compliant_name(data['tool']['poetry']['name'])
        return project_name


def execute_command(command: str) -> dict[str, str]:
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(stderr.decode())
        return {'command': command, 'result': stdout.decode()}


@task
def run(context: Context):
    context.run(f'python {get_project_path()}/main.py', pty=True)


@task
def test(context: Context):
    context.run('pytest . --cov=. --cov-report=xml', pty=True)


@task
def format_code(context: Context, verbose: bool = False) -> None:
    commands = [
        f'pautoflake {get_project_path()}',
        f'ruff --fix {get_project_path()}',
        f'yapf --in-place --recursive --parallel {get_project_path()}',
    ]
    results: list[dict[str, str]] = []
    with console.status('[bold green] Formatting code...'):
        for command in commands:
            results.append(execute_command(command))

    if verbose:
        for result in results:
            console.print(f'$ {result["command"]}')
            console.print(result['result'])

    console.print('[bold green]Success[/bold green]')


@task
def check(context: Context):
    check_code_style(context)
    check_types(context)


@task
def check_code_style(context: Context):
    commands = [
        f'pautoflake {get_project_path()} --check',
        f'ruff {get_project_path()}',
        f'yapf --diff --recursive --parallel {get_project_path()}',
    ]

    for command in commands:
        context.run(command, pty=True)


@task
def check_types(context: Context):
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
