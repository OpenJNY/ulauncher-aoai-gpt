import logging
import requests

from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction


logger = logging.getLogger(__name__)
EXTENSION_ICON = "images/icon.png"


def wrap_text(text, max_w):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) <= max_w:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    lines.append(current_line.strip())
    return "\n".join(lines)


class AOAIChatExtension(Extension):
    def __init__(self):
        super(AOAIChatExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        try:
            api_base = extension.preferences["api_base"]
            api_key = extension.preferences["api_key"]
            api_version = extension.preferences["api_version"]
            deployment_id = extension.preferences["deployment_id"]
            system_prompt = extension.preferences["system_prompt"]
            temperature = extension.preferences["temperature"]
            max_tokens = extension.preferences["max_tokens"]
            presence_penalty = extension.preferences["presence_penalty"]
            frequency_penalty = extension.preferences["frequency_penalty"]
            line_wrap = extension.preferences["line_wrap"]
        except Exception as err:
            err_msg = f"Failed to parse preferences: {err}"
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon=EXTENSION_ICON,
                        name=err_msg,
                        on_enter=CopyToClipboardAction(str(err)),
                    )
                ]
            )

        user_prompt = event.get_argument()
        logger.info("The search term is: %s", user_prompt)

        # Display blank prompt if user hasn't typed anything
        if not user_prompt:
            logger.info("Displaying blank prompt")
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon=EXTENSION_ICON,
                        name="Type in a prompt...",
                        on_enter=DoNothingAction(),
                    )
                ]
            )

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

        logger.info("Request:")
        logger.info(f"url: {url}")
        logger.info(f"headers: {headers}")
        logger.info(f"body: {body}")

        try:
            response = requests.post(url, headers=headers, json=body, timeout=10)
            logger.info("Response:")
            logger.info(response)
            choices = response.json()["choices"]
        except Exception as err:
            logger.error("Request failed: %s", str(err))
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon=EXTENSION_ICON,
                        name="Request failed: " + str(err),
                        on_enter=CopyToClipboardAction(str(err)),
                    )
                ]
            )

        items: list[ExtensionResultItem] = []
        try:
            for choice in choices:
                message = choice["message"]["content"]
                message = wrap_text(message, line_wrap)

                items.append(
                    ExtensionResultItem(
                        icon=EXTENSION_ICON,
                        name="Assistant",
                        description=message,
                        on_enter=CopyToClipboardAction(message),
                    )
                )
        # pylint: disable=broad-except
        except Exception as err:
            logger.error("Failed to parse response: %s", str(response))
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon=EXTENSION_ICON,
                        name="Failed to parse response: " + str(response),
                        on_enter=CopyToClipboardAction(str(err)),
                    )
                ]
            )

        try:
            item_string = " | ".join([item.description for item in items])
            logger.info("Results: %s", item_string)
        except Exception as err:
            logger.error("Failed to log results: %s", str(err))
            logger.error("Results: %s", str(items))

        return RenderResultListAction(items)


if __name__ == "__main__":
    AOAIChatExtension().run()
