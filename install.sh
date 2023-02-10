#!/bin/bash

# Get code from https://raw.githubusercontent.com/code-yeongyu/AiShell/master/aishell/main.py
curl -o main.py https://raw.githubusercontent.com/code-yeongyu/AiShell/master/aishell/main.py

# Install required packages using pip
pip install --upgrade typer[all] revchatgpt openai pydantic

# Make the python file executable
chmod +x main.py

# Move the file to environment path
sudo mv main.py /usr/local/bin/aishell
