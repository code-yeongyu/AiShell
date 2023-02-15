def make_executable_command(command: str) -> str:
    if command.startswith('\n'):
        command = command[1:]
    if command.endswith('\n'):
        command = command[:-1]
    if command.startswith('`'):
        command = command[1:]
    if command.endswith('`'):
        command = command[:-1]
    command = command.strip()
    command = command.split('User: ')[0]
    return command
