# AiShell 🤖

[![Release Package to PyPI](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml/badge.svg)](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml)
[![PyPI version](https://badge.fury.io/py/aishell.svg)](https://badge.fury.io/py/aishell)


A simple Python code that connects to OpenAI's ChatGPT and executes the returned results.

## Demo

![Demo](images/example.gif)

## Key Features 💡

- Interact with your computer using natural language
- Automatically executes the command from the response of ChatGPT
- Good for complex tasks like handling Git and extracting tar files
- No need to search StackOverflow for commands, AiShell has got you covered

## Installation 🔧

```sh
pip install aishell
```

## Usage 📝

```sh
aishell --help
```

## Prerequisites 📚

- Python 3.9.5
- Poetry
- OpenAI API Key

## Getting Started 🚀

### For those who want to use reverse-engineered `ChatGPT`

1. Login on <https://chat.openai.com/>
1. Get your 'accessToken` from <https://chat.openai.com/api/auth/session>
1. `export CHATGPT_ACCESS_KEY=<your access token>`
1. Enjoy AiShell

### For those who want to use `GPT-3`

1. Create account on OpenAI
1. Go to <https://platform.openai.com/account/api-keys>, Copy API key
1. Set the API key as an environment variable `OPENAI_API_KEY` or inject it directly into the code by editing it.
1. Enjoy AiShell

### For those who want to use Official ChatGPT API `gpt-3.5-turbo`

- Currently not supported, but soon will be supported!

## Contributions 💬

Feel free to contribute to AiShell by adding more functionality or fixing bugs.
