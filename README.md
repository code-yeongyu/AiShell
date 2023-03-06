# AiShell 🤖

[![codecov](https://codecov.io/gh/code-yeongyu/AiShell/branch/master/graph/badge.svg?token=MR72XGUQWJ)](https://codecov.io/gh/code-yeongyu/AiShell)
[![Release Package to PyPI](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml/badge.svg)](https://github.com/code-yeongyu/AiShell/actions/workflows/release.yml)
[![PyPI version](https://badge.fury.io/py/aishell.svg)](https://badge.fury.io/py/aishell)
[![Downloads](https://static.pepy.tech/personalized-badge/aishell?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/aishell)

A simple Python code that connects to OpenAI's ChatGPT and executes the returned results.

If you are interested in these projects, please checkout AiShell's brother project: [YGK-a](https://github.com/code-yeongyu/YGK-a). YGK-a is a client for the ChatGPT from your terminal, and also supports unix/linux pipelines.

## Demo

![Demo](https://raw.githubusercontent.com/code-yeongyu/AiShell/master/images/example.gif)

## Key Features 💡

- Interact with your computer using natural language
- Automatically executes the command from the response of ChatGPT
- Good for complex tasks like handling Git and extracting tar files
- No need to search StackOverflow for commands, `AiShell` has got you covered
- `AiShell` simplifies the process of setting up and retrieving tokens or API keys.
  - With `AiShell`, you don't have to worry about the technical details.
  - Simply install `AiShell`, execute it, and you're ready to go!

## Prerequisites 📚

- Python 3.9+
- ChatGPT Account (or OpenAI Account)

## Getting Started 🚀

To begin using `AiShell`, start by installing it with pip:

```sh
pip install aishell
```

Once you've installed `AiShell`, you can start using it right away.
For example, to print "Hello World" using `AiShell`, enter the following command:

```sh
aishell 'print Hello World'
```

## Advanced Settings 🛠

By default, `AiShell` is configured to use the reverse-engineered ChatGPT client and retrieve login information from your browser, so you don't need to configure anything to use `AiShell`. However, for those who want to use different models with an OpenAI API Key, you can configure it as follows:

1. Create an account on OpenAI.
1. Go to <https://platform.openai.com/account/api-keys> and copy your API key.
1. Modify or create the `~/.aishell_config.json` file as follows:

  ```json
  {
      ...
      "language_model": <language model of your preference>, //"official_chatgpt" or "gpt3"
      "openai_api_key": <your OpenAI API key>
  }
  ```

Here, you can specify the language model of your preference, such as "official_chatgpt" or "gpt3", and add your OpenAI API key. This will enable AiShell to use the specified language model and API key when executing commands.

## Contributions 💬

Feel free to contribute to `AiShell` by adding more functionality or fixing bugs.
