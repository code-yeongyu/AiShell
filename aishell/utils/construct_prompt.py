import os


def construct_prompt(query: str) -> str:
    return f'''
Translate the following task to a {os.uname()[0]} shell command. Users provide a text-query as input.
Provide ONLY the command in ONE LINE, with no explanation:

One-line command for: {query}
'''[1:]
