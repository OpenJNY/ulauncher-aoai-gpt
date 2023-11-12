# ulauncher-aoai-gpt

Ulauncher extension to generate text from caht models powered by Azure OpenAI, inspired by [ulauncher-gpt](https://github.com/seofernando25/ulauncher-gpt/).

## Preferences

| Key | Description | Default |
| --- | --- | --- |
| Keyword | Keyword to trigger the extension | `gpt` |
| API Endpoint | Azure OpenAI API endpoint | |
| API Key | Azure OpenAI API key | |
| API Version | Azure OpenAI API version | `2023-05-15` |
| Model Name | Azure OpenAI model name (deployment name) | `gpt-35-turbo` |
| Line Length | Maximum number of characters per line | 64 |
| System Prompt | Prompt to use for the system | `You are a helpful assistant.` |
| Temperature | Controls randomness. Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive. Higher temperature results in more random completions. | 1.0 |
| Max Tokens | Controls the number of tokens to generate. | 1024 |
| Frequency Penalty | How much to penalize new tokens based on their existing frequency in the text so far. Decreases the model's likelihood to repeat the same line verbatim. | 1.0 |
| Presence Penalty | How much to penalize new tokens based on whether they appear in the text so far. Decreases the model's likelihood to talk about the topic in general. | 1.0 |
