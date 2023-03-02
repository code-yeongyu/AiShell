# AiShell 🤖

[![Release Package to PyPI](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml/badge.svg)](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml)
[![PyPI version](https://badge.fury.io/py/aishell.svg)](https://badge.fury.io/py/aishell)


A simple Python code that connects to OpenAI's ChatGPT and executes the returned results.

## Demo

![Demo](https://raw.githubusercontent.com/code-yeongyu/AiShell/master/images/example.gif)

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

- Python 3
- OpenAI API Key or ChatGPT Account

## Getting Started 🚀

### For those who want to use reverse-engineered `ChatGPT`

- Permanent Login Method
    1. Login on <https://chat.openai.com/>
    1. Get your 'accessToken` from <https://chat.openai.com/api/auth/session>
    1. Set the API key as an environment variable `CHATGPT_ACCESS_TOKEN`
- Temporary Login Method
    1. Just run `aishell <query>`
    1. Browser opens up. Login there.
    1. Tell AiShell which browser you use.
    1. Enjoy AiShell

### For those who want to use `Official ChatGPT(GPT3.5-turbo)` or `GPT-3`

1. Create account on OpenAI
1. Go to <https://platform.openai.com/account/api-keys>, Copy API key
1. Set the API key as an environment variable `OPENAI_API_KEY`
1. Enjoy AiShell

## Contributions 💬

Feel free to contribute to AiShell by adding more functionality or fixing bugs.
