#!/bin/env python3

import requests
import dotenv
import os
import logging

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
dotenv.load_dotenv(dotenv_path)

api_base = os.environ.get("OPENAI_API_BASE", default="")
api_key = os.environ.get("OPENAI_API_KEY", default="")
api_version = os.environ.get("OPENAI_API_VERSION", default="")
deployment_id = "gpt-35-turbo"
system_prompt = "You are a helpful assistant."
user_prompt = "Does Azure OpenAI support customer managed keys?"
temperature = 1
max_tokens = 1024
presence_penalty = 0.6
frequency_penalty = 0.6

# https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#chat-completions

api_base = api_base.rstrip("/")
url = f"{api_base}/openai/deployments/{deployment_id}/chat/completions?api-version={api_version}"

headers = {
    "Content-Type": "application/json",
    "api-key": api_key,
}

body = {
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    "temperature": temperature,
    "max_tokens": max_tokens,
    "frequency_penalty": frequency_penalty,
    "presence_penalty": presence_penalty,
}

try:
    response = requests.post(url, headers=headers, json=body, timeout=10)
    answer = response.json()["choices"][0]
except Exception as err:
    logging.error(err)

print(answer)
