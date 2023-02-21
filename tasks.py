# type: ignore
import shutil

import toml
from invoke import Context, task
from invoke.exceptions import UnexpectedExit

import monkey_patch_invoke as _  # noqa: F401


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
def format_code(context: Context, verbose: bool = False):
    commands = [
        f'pautoflake {get_project_path()}',
        f'ruff --fix {get_project_path()}',
        f'yapf --in-place --recursive --parallel {get_project_path()}',
    ]

    for command in commands:
        context.run(command, pty=True)


@task
def check(context: Context):
    check_code_style(context)
    check_types(context)


@task
def check_code_style(context: Context):
    commands = [
        f'ruff {get_project_path()}',
        f'yapf --diff --recursive --parallel {get_project_path()}',
    ]

    for command in commands:
        context.run(command, pty=True)


@task
def check_types(context: Context):
    context.run(f'pyright {get_project_path()}', pty=True)


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


@task
def release(context: Context, version: str) -> None:
    '''Build & Publish to PyPI.'''

    # load pyproject
    pyproject_path = 'pyproject.toml'
    pyproject_string = ''
    with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
        pyproject_string = pyproject_file.read()
    pyproject = toml.loads(pyproject_string)
    # change version to today datetime
    pyproject['tool']['poetry']['version'] = version
    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        toml.dump(pyproject, pyproject_file)

    # build & publish
    try:
        context.run(
            '''
                poetry build --no-interaction
                poetry publish --no-interaction
            ''',
            pty=True,
        )
    except UnexpectedExit as exception:
        with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
            pyproject_file.write(pyproject_string)
        raise exception from exception

    # recover to original
    with open(pyproject_path, 'w', encoding='utf-8') as pyproject_file:
        pyproject_file.write(pyproject_string)
