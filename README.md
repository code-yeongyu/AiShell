# AiShell

A simple Python code that connects to OpenAI's ChatGPT and executes the returned results.

## Examples

### Simple Utility commands

![terminal example](images/aishell_example.png)

### A git helper

![terminal example](images/aishell_example2.png)

### A powerful git assistant: "add all files & amend last commit & push"

![terminal example3](images/aishell_example3.png)


## Prerequisites

- Python 3.9.5
- Poetry
- OpenAI API Key

## Getting Started

1. Create account on OpenAI
1. Go to <https://platform.openai.com/account/api-keys>, Copy API key
1. Set the API key as an environment variable OPENAI_API_KEY or inject it directly into the code by editing it.
1. Clone this repository to your local machine using git clone <repository-url>
1. Install the dependencies by running poetry install in your terminal
1. Start AiShell by running poetry run python3 aishell/main.py

## Contributions

Feel free to contribute to AiShell by adding more functionality or fixing bugs. Some suggestions for contributions include:

- Adding the ability to execute AiShell as a system command aishell <command>
- Publishing AiShell to PyPI so that others can easily download and use it
