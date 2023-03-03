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
- **No need to set up annoying retrieving of tokens or API keys with ChatGPT, as AiShell does it for you. INSTALL IT. EXECUTE IT. DONE.**

## Prerequisites 📚

- Python 3.9+
- ChatGPT Account (or OpenAI Account)

## Installation 🔧

```sh
pip install aishell
```

## Getting Started 🚀

Let's just start by printing "Hello World" using AiShell.

```sh
aishell 'print Hello World'
```

## Advanced Settings 🛠

### For those who want to use `Official ChatGPT(GPT3.5-turbo)` or `GPT-3`

1. Create account on OpenAI
1. Go to <https://platform.openai.com/account/api-keys>, Copy API key
1. Modify or create `~/.aishell/config.json` file like following

    ```sh
    {
        ...
        "language_model": <language model of your preference>, //"official_chatgpt" or "gpt3"
        "openai_api_key": <your openai api key>
    }
    ```

## Contributions 💬

Feel free to contribute to AiShell by adding more functionality or fixing bugs.
