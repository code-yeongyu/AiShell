from aishell.utils import make_executable_command


def test_make_executable_command_starts_and_ends_with_newline():
    command = '\nls -l\n'
    expected_output = 'ls -l'
    assert make_executable_command(command) == expected_output


def test_make_executable_command_starts_and_ends_with_backtick():
    command = '`python my_script.py`\n'
    expected_output = 'python my_script.py'
    assert make_executable_command(command) == expected_output


def test_make_executable_command_starts_with_user():
    command = 'User: cd ..'
    expected_output = 'cd ..'
    assert make_executable_command(command) == expected_output


def test_make_executable_command_no_leading_or_trailing_whitespace():
    command = 'git clone https://github.com/my_repo.git'
    expected_output = 'git clone https://github.com/my_repo.git'
    assert make_executable_command(command) == expected_output
